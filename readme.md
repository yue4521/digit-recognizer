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

## ドキュメント

詳細な情報については、以下のドキュメントを参照してください：

- [インストールガイド](docs/installation.md) - セットアップ手順
- [アーキテクチャ](docs/architecture.md) - システム構成詳細
- [API仕様](docs/api.md) - エンドポイント詳細
- [開発者ガイド](docs/development.md) - 開発環境とベストプラクティス
- [機械学習詳細](docs/ml-details.md) - モデルと前処理の詳細
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

## 利用可能なスクリプト

| スクリプト | 説明 |
|-----------|------|
| `npm run setup` | 完全セットアップ（依存関係 + モデル訓練） |
| `npm run dev` | 開発サーバー起動 |
| `npm run build` | 本番ビルド |
| `npm start` | 本番サーバー起動 |
| `npm run train-model` | SVMモデル訓練 |

## 技術スタック

- **フロントエンド**: React 18, CSS3
- **バックエンド**: Node.js, Express.js
- **機械学習**: Python, scikit-learn, PIL
- **データセット**: MNIST
- **開発ツール**: npm, venv

## プロジェクト構成

```
digit-recognizer/
├── client/          # Reactフロントエンド
├── server/          # Express.jsバックエンド
├── ml/              # Python機械学習
├── docs/            # ドキュメント
├── venv/            # Python仮想環境
└── package.json     # ルートスクリプト
```

## パフォーマンス

- モデル精度: 約95% (MNISTテストセット)
- 予測時間: 平均500ms
- サポート形式: JPEG, PNG
- ファイルサイズ制限: 2MB

## ブラウザサポート

- Chrome/Chromium (推奨)
- Firefox
- Safari
- Edge
- モバイルブラウザ

## セキュリティ

- ファイル形式検証 (JPEG/PNGのみ)
- ファイルサイズ制限 (最大2MB)
- 自動ファイル削除
- 入力検証とCORS保護

## トラブルシューティング

問題が発生した場合は[トラブルシューティングガイド](docs/troubleshooting.md)を参照してください。

### よくある問題

- モジュールエラー → `npm run install-all`
- Pythonエラー → 仮想環境の確認
- モデルエラー → `npm run train-model`
- ポート競合 → プロセス終了または.env設定

## ライセンス

MIT License

## 貢献

1. リポジトリをフォーク
2. 機能ブランチを作成
3. 変更をコミット
4. プルリクエストを作成

## 謝辞

- MNISTデータセット (Yann LeCun)
- scikit-learn
- React
- Express.js