# Changelog

このファイルでは、手書き数字認識アプリの主要な変更を記録しています。

## [1.0.0] - 2025-07-18

### 新機能
- 手書き数字認識のフルスタックWebアプリケーションを実装
- React 18を使用したモダンなフロントエンド
- Node.js/Express.jsによるRESTful API
- scikit-learnとSVMを使用した機械学習モデル
- MNISTデータセットによる数字認識
- ドラッグ&ドロップ対応の画像アップロード機能
- リアルタイム数字認識と信頼度スコア表示
- レスポンシブデザイン対応

### セキュリティ
- ファイル形式検証（JPEG/PNGのみ）
- ファイルサイズ制限（最大2MB）
- 自動ファイル削除機能
- CORS保護とInput検証

### ドキュメント
- 包括的なREADME.mdドキュメント
- 体系的なdocsフォルダ構造
  - インストールガイド
  - API仕様書
  - アーキテクチャ説明
  - 開発者ガイド
  - 機械学習詳細説明
  - トラブルシューティングガイド

### 開発環境
- npm scriptsによる統合開発環境
- Python仮想環境サポート
- concurrentlyによる並行開発サーバー起動
- ESLintとPrettierによるコード品質管理

### 修正内容
- sklearn バージョン不整合による認識精度問題を解決
- npm run dev終了時のプロセス残存問題を解決
- 信頼度表示エラー（917%表示）を修正
- 仮想環境でのポート競合エラーを修正

### 技術スタック
- フロントエンド: React 18, CSS3
- バックエンド: Node.js, Express.js, Multer
- 機械学習: Python 3.8+, scikit-learn, PIL, NumPy
- データセット: MNIST手書き数字データセット
- 開発ツール: ESLint, Prettier, concurrently, nodemon

### パフォーマンス
- モデル精度: 約95% (MNISTテストセット)
- 予測時間: 平均500ms
- サポート形式: JPEG, PNG
- ファイルサイズ制限: 2MB

### ブラウザサポート
- Chrome/Chromium (推奨)
- Firefox
- Safari
- Edge
- モバイルブラウザ