# 開発者ガイド

## 開発環境のセットアップ

### 必要なツール

- Node.js (v14以上)
- Python (3.8以上)
- Git
- エディタ (VS Code推奨)

### 開発サーバーの起動

```bash
# 全てのサーバーを同時起動
npm run dev

# 個別起動
npm run dev-server    # バックエンドのみ
npm run dev-client    # フロントエンドのみ
```

## 利用可能なスクリプト

### ルートディレクトリ

| スクリプト | 説明 |
|-----------|------|
| `npm run setup` | 完全セットアップ（依存関係 + モデル訓練） |
| `npm run install-all` | Node.js依存関係をインストール |
| `npm run install-python` | Python依存関係をインストール |
| `npm run train-model` | SVMモデルを訓練 |
| `npm run dev` | 開発サーバー起動 |
| `npm run build` | 本番ビルド |
| `npm start` | 本番サーバー起動 |

### フロントエンド (client/)

| スクリプト | 説明 |
|-----------|------|
| `npm start` | React開発サーバー起動 |
| `npm run build` | 本番用ビルド |
| `npm test` | テスト実行 |
| `npm run eject` | Create React Appから切り離し |

### バックエンド (server/)

| スクリプト | 説明 |
|-----------|------|
| `npm start` | Expressサーバー起動 |
| `npm run dev` | nodemonで起動（自動再読み込み） |

## コーディング規約

### JavaScript/React

- ES6+ 構文を使用
- 関数コンポーネントとHooksを優先
- 適切なエラーハンドリングを実装
- console.logは本番前に削除

### Python

- PEP 8 スタイルガイドに従う
- 型ヒントの使用を推奨
- docstringでドキュメント化
- エラーハンドリングを適切に実装

### Git

- Semantic Commit Messagesを使用
- 日本語でコミットメッセージを記述
- featureブランチで開発

## テスト手順

### 機械学習モデルのテスト

```bash
cd ml
python3 predict.py path/to/test/image.png
```

### APIエンドポイントのテスト

```bash
# ヘルスチェック
curl http://localhost:5000/api/health

# 画像予測
curl -X POST -F "image=@test.png" http://localhost:5000/api/predict
```

### フロントエンドのテスト

```bash
cd client
npm test
```

## デバッグ

### フロントエンド

- ブラウザのDevToolsを使用
- React Developer Toolsの活用
- console.logでデータフローを確認

### バックエンド

- nodemonで自動再読み込み
- console.logでリクエスト/レスポンスを確認
- PostmanでAPI直接テスト

### Python/機械学習

- print文でデバッグ情報を出力
- PILで画像変換過程を確認
- モデルの信頼度スコアを監視

## 新機能の追加

### フロントエンド機能

1. `client/src/App.jsx`を編集
2. 必要に応じてCSS追加
3. APIとの連携を確認
4. レスポンシブ対応をテスト

### バックエンド機能

1. `server/routes/`に新しいルートを追加
2. `server/index.js`でルートを登録
3. エラーハンドリングを実装
4. CORS設定を確認

### 機械学習機能

1. `ml/`に新しいスクリプトを追加
2. requirements.txtを更新
3. モデルの再訓練が必要か確認
4. パフォーマンスをテスト

## パフォーマンス最適化

### フロントエンド

- 画像の最適化
- 不要な再レンダリングの防止
- バンドルサイズの監視

### バックエンド

- ファイルサイズ制限の調整
- メモリ使用量の監視
- レスポンス時間の測定

### 機械学習

- モデルサイズの最適化
- 予測時間の短縮
- メモリ効率の改善

## ベストプラクティス

### セキュリティ

- ファイル検証の徹底
- 入力サニタイゼーション
- 秘密情報の環境変数化

### 保守性

- コードコメントの適切な使用
- モジュールの分割
- エラーメッセージの統一

### 可読性

- 意味のある変数名
- 適切な関数分割
- 一貫性のあるコーディングスタイル