Pocket Turbo Racer v27 GitHub Pages ready

v27をベースに、GitHub Pages反映時のService Workerキャッシュ名をv27用に更新しました。

主な変更:
- 車画像ファイル名を安全名へ変更
- HTML内の spriteId / carId も安全名へ変更
- v16の車画像改善とオープニング車拡大は維持
- レース開始、カウントダウン、BGM、速度0.98は維持

車名:
AERO / NOVA / DART / CRUX / VELA / BOLT

主な画像:
assets/cars/shop/aero.png
assets/cars/shop/nova.png
assets/cars/shop/dart.png
assets/cars/shop/crux.png
assets/cars/shop/vela.png
assets/cars/bolt.png

確認方法:
1. このフォルダで PowerShell を開く
2. python -m http.server 8000
3. http://localhost:8000 を開く
4. Ctrl + F5
5. START演出、Garage、Race Setup、カウントダウン、レース開始を確認

GitHub Pagesへ反映する場合:
このフォルダの中身を GitHub のリポジトリに上書きアップロードしてください。


v18変更:
- AERO と VELA の画像を入れ替え
- NOVA と CRUX の画像を入れ替え
- レース中の車画像を crisp 表示へ戻し、少し小さめに調整
- 安全名ファイル構成は維持


v19変更:
- レース中の車の黒い丸い影を削除
- オープニングのロゴ点滅を追加
- オープニング画面の上下の緑背景を、レース中の芝生風ドット背景に変更
- v18の車画像入れ替えは維持


v20変更:
- オープニング画面の上下の緑エリアに、黒い点のドット絵を追加
- ロゴ点滅は維持
- 芝生風背景は維持
- レース中の黒い丸い影削除は維持


v21変更:
- Garage / Course Select / Race Setup / Result などの画面まわりを、緑＋黒ドットの芝生風背景に統一
- オープニング画面の緑部分も同じ芝生カラーへ統一
- ロゴ点滅は維持
- 黒い点のドット絵は維持
- レース中の車まわりの黒い丸い影削除は維持


v22変更:
- オープニング画面の緑部分全体に黒いドットを入れるよう修正
- ドットが一部だけになる状態を修正
- v21の全体芝生テーマは維持


v23変更:
- オープニングの文字ロゴを、アップロードされたロゴ画像に差し替え
- ロゴ点滅は画像ロゴに対して維持
- STARTボタン、タイトル車、緑背景、黒ドットは維持
- ロゴ画像ファイル: assets/ui/title-logo-v23.png


v24変更:
- ロゴ画像の背景を透過化
- 透過ロゴファイル: assets/ui/title-logo-v24-transparent.png
- オープニングロゴを道路枠いっぱいに近い大きさまで拡大
- ロゴ点滅は維持


v25変更:
- 透過ロゴの透明余白をカット
- 新ロゴファイル: assets/ui/title-logo-v25-cropped.png
- オープニングロゴをかなり大きく調整
- ロゴに使う横幅を増やすようタイトル画面レイアウトも調整


v26変更:
- Race Setup の CAR と COURSE の横並び位置を調整
- 車名＋車画像 と コース名＋ミニMAP の高さバランスを修正
- デスクトップ表示とスマホ横画面表示の両方を微調整


v27変更:
- Race Setup のコース名を車種名に合わせて少し上へ
- ミニMAPを車画像に合わせて少し下へ
- 車側の位置は変更なし
