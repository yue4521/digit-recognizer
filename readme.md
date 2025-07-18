# 🔢 手書き数字認識アプリ

機械学習を使用して手書き数字（0-9）を認識するフルスタックWebアプリケーションです。ユーザーはReactフロントエンドを通じて手書き数字の画像をアップロードし、訓練済みのSVMモデルを使用して数字を予測できます。

## 🌟 主な機能

- **🖼️ 画像アップロード**: ドラッグ&ドロップまたはクリックでファイルをアップロード
- **📱 レスポンシブデザイン**: デスクトップとモバイルデバイスでシームレスに動作
- **🤖 AI搭載認識**: MNISTデータセットで訓練されたSVMモデルを使用
- **⚡ リアルタイム処理**: 高速な予測と信頼度スコア
- **🎨 モダンUI**: 美しいグラデーションインターフェースとスムーズなアニメーション
- **🔒 セキュリティ**: 自動ファイル削除と入力検証

## 🏗️ アーキテクチャ

### フロントエンド（React）
- **ポート**: 3000
- **フレームワーク**: React 18
- **機能**: ドラッグ&ドロップアップロード、画像プレビュー、ローディング状態、エラーハンドリング

### バックエンド（Node.js + Express）
- **ポート**: 5000
- **フレームワーク**: Express.js
- **機能**: ファイルアップロード処理、Pythonスクリプト連携、CORS対応

### 機械学習（Python）
- **モデル**: サポートベクターマシン（SVM）
- **データセット**: MNIST手書き数字データセット
- **ライブラリ**: scikit-learn, PIL, numpy

## 📁 プロジェクト構成

```
digit-recognizer/
├── client/                 # Reactフロントエンド
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.jsx         # メインReactコンポーネント
│   │   ├── App.css         # スタイリング
│   │   ├── index.js        # Reactエントリーポイント
│   │   └── index.css       # グローバルスタイル
│   └── package.json
├── server/                 # Node.jsバックエンド
│   ├── routes/
│   │   └── predict.js      # 予測APIエンドポイント
│   ├── index.js            # Expressサーバー
│   └── package.json
├── ml/                     # Python機械学習コンポーネント
│   ├── train_model.py      # モデル訓練スクリプト
│   ├── predict.py          # 予測スクリプト
│   ├── requirements.txt    # Python依存関係
│   └── svm_model.pkl       # 訓練済みモデル（生成される）
├── venv/                   # Python仮想環境
├── .env.example           # 環境変数テンプレート
├── .gitignore             # Git除外ルール
├── package.json           # ルートpackage.jsonとスクリプト
└── README.md              # このファイル
```

## 🚀 クイックスタート

### 前提条件

- **Node.js**（v14以上）
- **Python**（3.8以上）
- **npm**または**yarn**

### インストール

1. **リポジトリをクローン**:
   ```bash
   git clone <リポジトリURL>
   cd digit-recognizer
   ```

2. **Python仮想環境を設定**:
   ```bash
   python3 -m venv venv
   
   # Windows:
   venv\Scripts\activate
   
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **すべての依存関係をインストールしてモデルを訓練**:
   ```bash
   npm run setup
   ```

   このコマンドは以下を実行します：
   - フロントエンドとバックエンドのNode.js依存関係をインストール
   - 仮想環境にPython依存関係をインストール
   - MNISTデータセットでSVMモデルを訓練

### 開発

1. **開発サーバーを起動**:
   ```bash
   npm run dev
   ```

   これにより以下が起動します：
   - バックエンドサーバー `http://localhost:5000`
   - フロントエンドサーバー `http://localhost:3000`

2. **個別にサーバーを起動**:
   ```bash
   # バックエンドのみ
   npm run dev-server
   
   # フロントエンドのみ
   npm run dev-client
   ```

### 本番ビルド

1. **Reactアプリをビルド**:
   ```bash
   npm run build
   ```

2. **本番サーバーを起動**:
   ```bash
   npm start
   ```

## 📋 利用可能なスクリプト

### ルートディレクトリ

- `npm run setup` - 完全セットアップ（依存関係インストール + モデル訓練）
- `npm run install-all` - Node.js依存関係をインストール
- `npm run install-python` - Python依存関係をインストール
- `npm run train-model` - SVMモデルを訓練
- `npm run dev` - フロントエンドとバックエンドを開発モードで起動
- `npm run dev-server` - バックエンドのみ起動
- `npm run dev-client` - フロントエンドのみ起動
- `npm run build` - Reactアプリを本番用にビルド
- `npm start` - 本番サーバーを起動

### フロントエンド（client/）

- `npm start` - React開発サーバーを起動
- `npm run build` - 本番用にビルド
- `npm test` - テストを実行
- `npm run eject` - Create React Appから切り離し

### バックエンド（server/）

- `npm start` - Expressサーバーを起動
- `npm run dev` - nodemonで起動（自動再読み込み）

## 🔧 環境変数

`.env.example`を基に`.env`ファイルをルートディレクトリに作成：

```env
# サーバー設定
PORT=5000
NODE_ENV=development

# Python環境
PYTHON_PATH=venv/bin/python3
```

## 🧠 機械学習の詳細

### モデル訓練

SVMモデルはMNISTデータセットで訓練されます：
- **訓練サンプル**: 8,000画像
- **検証サンプル**: 2,000画像
- **特徴量**: 784（28x28ピクセル値）
- **クラス**: 10（数字0-9）
- **カーネル**: RBF（放射基底関数）

### 画像前処理

`predict.py`スクリプトはアップロードされた画像を前処理します：

1. **グレースケール変換** - 単一チャンネルに変換
2. **背景色検出** - 背景が黒か白かを検出
3. **色反転** - 黒背景に白い数字を確保
4. **正方形パディング** - 画像を正方形にするためのパディング追加
5. **リサイズ** - 28x28ピクセル（MNIST標準）にスケール
6. **正規化** - ピクセル値を0-1の範囲にスケール

### 予測プロセス

1. ユーザーがReactフロントエンド経由で画像をアップロード
2. Expressサーバーがmulter経由で画像を受信
3. 画像を一時保存
4. Pythonスクリプトが画像を処理して予測を実行
5. 信頼度スコア付きの結果をJSONで返却
6. 一時ファイルを自動削除

## 📡 APIエンドポイント

### POST /api/predict

数字認識用の画像をアップロード。

**リクエスト:**
- メソッド: `POST`
- コンテンツタイプ: `multipart/form-data`
- ボディ: `image`フィールドを含むフォームデータ

**レスポンス:**
```json
{
  "success": true,
  "prediction": 7,
  "confidence": 0.95,
  "filename": "example.png"
}
```

**エラーレスポンス:**
```json
{
  "error": "予測に失敗しました",
  "message": "エラーの詳細"
}
```

### GET /api/health

ヘルスチェックエンドポイント。

**レスポンス:**
```json
{
  "status": "サーバーが実行中です",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

## 🛠️ 開発のコツ

### 新しいモデルの訓練

異なるパラメータでモデルを再訓練したい場合：

```bash
cd ml
python3 train_model.py
```

### Pythonスクリプトのテスト

予測スクリプトを直接テスト：

```bash
cd ml
python3 predict.py path/to/your/image.png
```

### デバッグ

- バックエンドの問題についてはサーバーログを確認
- フロントエンドのデバッグはブラウザのDevToolsを使用
- 機械学習の問題についてはPythonスクリプトの出力を確認

## 🌐 ブラウザサポート

- Chrome/Chromium（推奨）
- Firefox
- Safari
- Edge

## 📱 モバイルサポート

アプリケーションは完全にレスポンシブで以下で動作します：
- iOS Safari
- Android Chrome
- Mobile Firefox

## 🔒 セキュリティ機能

- ファイル形式検証（JPEG/PNGのみ）
- ファイルサイズ制限（最大2MB）
- アップロードされたファイルの自動削除
- 入力サニタイゼーション
- CORS保護

## 🚨 トラブルシューティング

### よくある問題

1. **「モジュールが見つかりません」エラー**:
   - `npm run install-all`を実行して依存関係をインストール

2. **Pythonスクリプトが失敗する**:
   - 仮想環境がアクティブになっていることを確認
   - `pip install -r ml/requirements.txt`を実行

3. **モデルファイルが見つからない**:
   - `npm run train-model`を実行してモデルを生成

4. **ポートが既に使用中**:
   - .envファイルでPORTを変更
   - ポート3000/5000の既存プロセスを終了

### プラットフォーム固有の問題

**Windows**:
- `source venv/bin/activate`の代わりに`venv\Scripts\activate`を使用
- PythonがPATHに追加されていることを確認

**macOS/Linux**:
- `python`の代わりに`python3`を使用
- スクリプト実行の適切な権限を確認

## 📊 パフォーマンス

- **モデル精度**: MNISTテストセットで約95%
- **予測時間**: 平均約500ms
- **ファイルアップロード制限**: 2MB
- **サポート形式**: JPEG, PNG

## 🤝 貢献

1. リポジトリをフォーク
2. 機能ブランチを作成
3. 変更をコミット
4. ブランチにプッシュ
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。

## 🙏 謝辞

- MNISTデータセット：Yann LeCun氏
- 機械学習ツール：scikit-learn
- 素晴らしいフレームワーク：Reactチーム
- Webフレームワーク：Express.js