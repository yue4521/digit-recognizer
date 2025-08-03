# インストールガイド

## 前提条件

- Node.js (v14以上)
- Python (3.8以上)
- npm または yarn

## インストール手順

### 1. リポジトリをクローン

```bash
git clone <リポジトリURL>
cd digit-recognizer
```

### 2. Python仮想環境を設定

```bash
python3 -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### 3. 完全セットアップの実行

```bash
npm run setup
```

このコマンドは以下を実行します：
- フロントエンドとバックエンドのNode.js依存関係をインストール
- 仮想環境にPython依存関係をインストール
- MNISTデータセットでSVMモデルを訓練

## 個別インストール

### Node.js依存関係のみ

```bash
npm run install-all
```

### Python依存関係のみ

```bash
npm run install-python
```

### モデル訓練のみ

```bash
npm run train-model
```

## 環境変数の設定

`.env.example`を基に`.env`ファイルをルートディレクトリに作成：

```env
# サーバー設定
PORT=5000
NODE_ENV=development

# Python環境
PYTHON_PATH=venv/bin/python3
```

## 動作確認

### 開発サーバーの起動

```bash
npm run dev
```

以下のサーバーが起動します：
- バックエンドサーバー: http://localhost:5000
- フロントエンドサーバー: http://localhost:3000

### 個別サーバー起動

```bash
# バックエンドのみ
npm run dev-server

# フロントエンドのみ
npm run dev-client
```

## プラットフォーム固有の注意事項

### Windows

- `source venv/bin/activate`の代わりに`venv\Scripts\activate`を使用
- PythonがPATHに追加されていることを確認

### macOS/Linux

- `python`の代わりに`python3`を使用
- スクリプト実行の適切な権限を確認