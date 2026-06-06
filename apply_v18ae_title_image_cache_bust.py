from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path.cwd()
index_path = ROOT / "index.html"
sw_path = ROOT / "service-worker.js"
report_path = ROOT / "v18ae_title_image_cache_bust_report.txt"

if not index_path.exists():
    raise SystemExit("index.html が見つかりません。このスクリプトを pocket-turbo-racer / pocket-car-racer フォルダ直下で実行してください。")

html = index_path.read_text(encoding="utf-8")
backup_now = ROOT / "index_backup_before_v18ae_title_image_cache_bust.html"
if not backup_now.exists():
    backup_now.write_text(html, encoding="utf-8")

changed = []
errors = []
notes = []

# 目的:
# v18q で assets が復元/上書きされた可能性がある。
# PCは正常でAndroid WebViewだけタイトル車が古い/巨大な表示なら、Service Worker/画像キャッシュが原因の可能性が高い。
# タイトル車画像だけに ?v=18ae を付け、Androidが古い画像キャッシュを使わないようにする。
# NEONやCPU処理、レース処理、タイトルCSSは触らない。

def strip_query(src: str) -> str:
    return src.split("?", 1)[0]

m = re.search(r'<div class="titleCars" aria-hidden="true">[\s\S]*?</div>', html)
if not m:
    raise SystemExit("titleCars ブロックが見つかりませんでした。")

block = m.group(0)

def add_title_cache_bust(match):
    tag = match.group(0)
    src = match.group(1)
    clean = strip_query(src)
    # タイトル車だけ cache-bust。存在確認はsrcがassets始まりなら不要。
    new_src = clean + "?v=18ae-title"
    return tag.replace(f'src="{src}"', f'src="{new_src}"')

new_block = re.sub(r'<img\b[^>]*\bsrc="([^"]+)"[^>]*>', add_title_cache_bust, block)

if new_block != block:
    html = html[:m.start()] + new_block + html[m.end():]
    changed.append("added cache-busting query to title car images")
else:
    notes.append("title car image src already unchanged or no img found")

# 追加で、起動時に古いService Worker cacheを掃除する軽いJSを入れる。
# Android WebViewで古い画像キャッシュが残るケースを潰す。
clear_js = """
<script>
(function(){
  try {
    var KEY = 'ptrTitleCacheBust18aeDone';
    if (!localStorage.getItem(KEY) && window.caches && caches.keys) {
      caches.keys().then(function(keys){
        return Promise.all(keys.map(function(k){
          if (String(k).indexOf('pocket-turbo-racer-') === 0) return caches.delete(k);
          return false;
        }));
      }).then(function(){ localStorage.setItem(KEY, '1'); });
    }
  } catch (e) {}
})();
</script>
"""

if "ptrTitleCacheBust18aeDone" not in html:
    html = html.replace("</head>", clear_js + "\n</head>", 1)
    changed.append("added one-time Service Worker cache cleanup for Android/WebView")
else:
    notes.append("cache cleanup JS already exists")

index_path.write_text(html, encoding="utf-8")

# service-worker cache更新
if sw_path.exists():
    sw = sw_path.read_text(encoding="utf-8")
    new_sw = re.sub(
        r'const CACHE_NAME = ".*?";',
        'const CACHE_NAME = "pocket-turbo-racer-v18ae-title-image-cache-bust";',
        sw,
        count=1,
    )
    if new_sw != sw:
        sw_path.write_text(new_sw, encoding="utf-8")
        changed.append("service worker cache updated to v18ae")
else:
    errors.append("service-worker.js not found")

# check
html2 = index_path.read_text(encoding="utf-8")
checks = []
checks.append(("titleCars exists", '<div class="titleCars" aria-hidden="true">' in html2))
checks.append(("title image cache bust exists", "?v=18ae-title" in html2))
checks.append(("cache cleanup JS exists", "ptrTitleCacheBust18aeDone" in html2))

scripts = re.findall(r"<script[^>]*>([\s\S]*?)</script>", html2, flags=re.IGNORECASE)
if scripts:
    with tempfile.TemporaryDirectory() as td:
        js_path = Path(td) / "inline.js"
        js_path.write_text("\n;\n".join(scripts), encoding="utf-8")
        try:
            result = subprocess.run(["node", "--check", str(js_path)], text=True, capture_output=True, timeout=20)
            checks.append(("JavaScript syntax node --check", result.returncode == 0))
            if result.returncode != 0:
                errors.append((result.stderr or result.stdout).strip())
        except FileNotFoundError:
            notes.append("Node.js not found; JS syntax check skipped")
else:
    errors.append("No inline scripts found")

if sw_path.exists():
    sw2 = sw_path.read_text(encoding="utf-8")
    checks.append(("service worker v18ae", "pocket-turbo-racer-v18ae-title-image-cache-bust" in sw2))

for name, ok in checks:
    if not ok:
        errors.append(name)

report = []
report.append("v18ae title image cache bust report")
report.append("=" * 40)
report.append("")
report.append("Changed:")
report.extend(["- " + c for c in changed] or ["- no changes"])
report.append("")
report.append("Notes:")
report.extend(["- " + n for n in notes] or ["- none"])
report.append("")
report.append("Checks:")
for name, ok in checks:
    report.append(f"- {name}: " + ("OK" if ok else "NG"))
report.append("")
report.append("Result: " + ("OK" if not errors else "NG"))
if errors:
    report.append("Errors:")
    report.extend(["- " + str(e) for e in errors])

text = "\n".join(report)
report_path.write_text(text, encoding="utf-8")
print(text)
print("")
print("現在バックアップ:", backup_now.name)
print("レポート:", report_path.name)
