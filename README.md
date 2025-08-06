# 手書き数字認識アプリ

[![Version](https://img.shields.io/badge/version-v1.1.0-blue.svg)](https://github.com/yue4521/digit-recognizer/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENCE)
[![React](https://img.shields.io/badge/React-19.1.1-61DAFB?logo=react)](https://reactjs.org/)
[![Node.js](https://img.shields.io/badge/Node.js-Latest-339933?logo=node.js)](https://nodejs.org/)
[![Express](https://img.shields.io/badge/Express-5.1.0-000000?logo=express)](https://expressjs.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?logo=javascript)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

機械学習を使用して手書き数字（0-9）を認識するフルスタックWebアプリケーションです。

## 概要

React フロントエンド、Node.js/Express バックエンド、Python機械学習の3層構成で構築された手書き数字認識システムです。MNISTデータセットで訓練されたSVMモデルを使用して画像の数字を予測します。

## 主な機能

- 画像アップロード（ドラッグ&ドロップ対応）
- リアルタイム数字認識
- 信頼度スコア表示
- レスポンシブデザイン
- セキュリティ機能

## ドキュメント

詳細な情報については、以下のドキュメントを参照してください：

- [インストールガイド](docs/installation.md) - セットアップ手順
- [アーキテクチャ](docs/architecture.md) - システム構成詳細
- [API仕様](docs/api.md) - エンドポイント詳細
- [開発者ガイド](docs/development.md) - 開発環境とベストプラクティス
- [機械学習詳細](docs/ml-details.md) - モデルと前処理の詳細
- [クイックリファレンス](docs/quick-reference.md) - スクリプト一覧とパフォーマンス
- [ブラウザサポート](docs/browser-support.md) - 対応ブラウザ詳細
- [セキュリティ](docs/security.md) - セキュリティ機能詳細
- [貢献ガイド](docs/contributing.md) - 貢献方法とガイドライン
- [トラブルシューティング](docs/troubleshooting.md) - よくある問題と解決方法

## クイックスタート

### 前提条件

- Node.js (v14以上)
- Python (3.8以上)
- npm

### 簡単セットアップ

```bash
# リポジトリをクローン
git clone <リポジトリURL>
cd digit-recognizer

# Python仮想環境を作成
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 完全セットアップ実行
npm run setup

# 開発サーバー起動
npm run dev
```

ブラウザで http://localhost:3000 にアクセスしてアプリケーションを使用できます。

## 技術スタック

- **フロントエンド**: React 18, CSS3
- **バックエンド**: Node.js, Express.js
- **機械学習**: Python, scikit-learn, PIL
- **データセット**: MNIST

詳細な情報は[クイックリファレンス](docs/quick-reference.md)を参照してください。

## ライセンス

MIT License