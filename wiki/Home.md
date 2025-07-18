# 手書き数字認識アプリ

機械学習を使用して手書き数字（0-9）を認識するフルスタックWebアプリケーションです。

## 概要

React フロントエンド、Node.js/Express バックエンド、Python機械学習の3層構成で構築された手書き数字認識システムです。MNISTデータセットで訓練されたSVMモデルを使用して画像の数字を予測します。

## 主な機能

- 画像アップロード（ドラッグ&ドロップ対応）
- リアルタイム数字認識
- 信頼度スコア表示
- レスポンシブデザイン
- セキュリティ機能

## クイックスタート

### 前提条件

- Node.js (v14以上)
- Python (3.8以上)
- npm

### 簡単セットアップ

```bash
# リポジトリをクローン
git clone https://github.com/yue4521/digit-recognizer.git
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

## ドキュメント

- [Installation](Installation) - インストールガイド
- [API Reference](API-Reference) - API仕様
- [Architecture](Architecture) - システム構成
- [Development Guide](Development-Guide) - 開発者ガイド
- [ML Details](ML-Details) - 機械学習詳細
- [Troubleshooting](Troubleshooting) - トラブルシューティング

## 技術スタック

- **フロントエンド**: React 18, CSS3
- **バックエンド**: Node.js, Express.js
- **機械学習**: Python, scikit-learn, PIL
- **データセット**: MNIST
- **開発ツール**: npm, venv

## パフォーマンス

- モデル精度: 約95% (MNISTテストセット)
- 予測時間: 平均500ms
- サポート形式: JPEG, PNG
- ファイルサイズ制限: 2MB

## セキュリティ

- ファイル形式検証 (JPEG/PNGのみ)
- ファイルサイズ制限 (最大2MB)
- 自動ファイル削除
- 入力検証とCORS保護

## ライセンス

MIT License