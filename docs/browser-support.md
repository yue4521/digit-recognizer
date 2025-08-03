# ブラウザサポート

手書き数字認識アプリがサポートするブラウザの詳細情報です。

## 対応ブラウザ

### デスクトップ

- **Chrome/Chromium** (推奨)
  - 最新版での動作を推奨
  - Canvas APIとFile APIの完全サポート
- **Firefox**
  - バージョン 80 以上
- **Safari**
  - バージョン 14 以上
  - macOS/iOS対応
- **Microsoft Edge**
  - Chromiumベース版

### モバイル

- **モバイルブラウザ**
  - iOS Safari
  - Android Chrome
  - Samsung Internet

## 必要な機能

アプリケーションが正常に動作するために必要なブラウザ機能：

- **File API** - ファイルアップロード
- **Canvas API** - 画像処理
- **Fetch API** - サーバー通信
- **ES6+ JavaScript** - モダンJavaScript機能

## 既知の制限事項

- Internet Explorer はサポートしていません
- 古いモバイルブラウザ（iOS 12以前、Android 5以前）では制限があります
- JavaScript無効環境では動作しません

## 推奨設定

最適な体験のために以下を推奨します：

- JavaScript有効
- Cookie有効
- ローカルストレージ有効
- 最新のブラウザバージョン