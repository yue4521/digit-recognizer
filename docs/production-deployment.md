# 本番環境への配置準備

## セキュリティ修正完了状況

### ✅ 修正済み脆弱性

#### フェーズ1: 致命的脆弱性 (Critical)
- [x] **Pickle逆シリアル化脆弱性** (ml/predict.py:127)
  - SHA256ハッシュによるモデルファイル整合性検証
  - 悪意あるモデルファイルの読み込み防止
  - 開発環境では警告表示、本番環境では厳格な検証

- [x] **コマンドインジェクション脆弱性** (server/routes/predict.js:72)
  - Python実行パスのホワイトリスト制御
  - パストラバーサル攻撃の防止
  - 環境変数の検証強化

#### フェーズ2: 高リスク脆弱性 (High)
- [x] **認証・認可システム実装**
  - API キー認証の導入 (server/middleware/auth.js)
  - レート制限機能 (15分間に100リクエスト)
  - 不正アクセス検出とログ記録

- [x] **ファイル検証・入力検証強化**
  - ファイル署名（マジックナンバー）検証
  - パストラバーサル対策
  - ファイルサイズ制限 (100 bytes - 5MB)
  - アップロードディレクトリ外アクセス防止

- [x] **CORS設定適正化**
  - 明示的な許可ドメイン設定
  - HTTPメソッド制限 (GET, POST)
  - 適切なヘッダー制御

#### フェーズ3: 中・低リスク脆弱性 (Medium/Low)
- [x] **セキュリティヘッダー実装**
  - CSP (Content Security Policy)
  - X-Frame-Options: DENY
  - X-Content-Type-Options: nosniff
  - X-XSS-Protection: 1; mode=block
  - Referrer-Policy: strict-origin-when-cross-origin

- [x] **レート制限実装**
  - メモリベースのレート制限
  - クライアント別制限管理
  - 制限超過時の適切なレスポンス

- [x] **エラーハンドリング改善**
  - 本番環境での詳細エラー情報隠蔽
  - セキュリティエラーの適切な分類
  - 内部ログとユーザー向けメッセージの分離

- [x] **依存関係脆弱性対応**
  - サーバー依存関係: 脆弱性なし
  - クライアント依存関係: 開発環境のみの脆弱性を特定
  - 本番ビルドには影響なし

## 本番環境配置前チェックリスト

### 1. 環境設定
- [ ] `.env` ファイルの適切な設定
  - [ ] `NODE_ENV=production` の設定
  - [ ] 強力なAPIキーの生成と設定
  - [ ] 許可ドメインの適切な設定
  - [ ] Pythonパスの確認
- [ ] MLモデルファイルの整合性ハッシュ値設定
- [ ] ログファイルパスとパーミッションの確認

### 2. インフラストラクチャ
- [ ] HTTPS/TLS設定の確認
- [ ] リバースプロキシ (Nginx/Apache) の設定
- [ ] ファイアウォール設定
- [ ] アップロードディレクトリのパーミッション設定
- [ ] ログローテーションの設定

### 3. セキュリティ検証
- [ ] 全APIエンドポイントの認証確認
- [ ] レート制限の動作確認
- [ ] ファイルアップロード制限の確認
- [ ] エラーレスポンスの情報漏洩チェック
- [ ] CORS設定の動作確認

### 4. パフォーマンス
- [ ] MLモデルの読み込み時間確認
- [ ] 画像処理のレスポンス時間測定
- [ ] メモリ使用量の監視設定
- [ ] CPU使用率の監視設定

### 5. 監視・ログ
- [ ] アプリケーションログの設定
- [ ] エラー監視の設定
- [ ] セキュリティイベントの監視
- [ ] パフォーマンス監視の設定

## 推奨本番環境構成

### アプリケーション構成
```
Internet → Load Balancer → Reverse Proxy (Nginx) → Node.js Server
                                                  → ML Service (Python)
```

### セキュリティ層
1. **ネットワーク層**: ファイアウォール、DDoS保護
2. **アプリケーション層**: API認証、レート制限、入力検証
3. **データ層**: ファイル検証、モデル整合性チェック

### 環境変数設定例
```bash
NODE_ENV=production
PORT=5002
API_KEY=<32文字以上のランダムキー>
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
PYTHON_PATH=/usr/bin/python3
ALLOWED_MODEL_HASHES=<モデルファイルのSHA256ハッシュ>
LOG_LEVEL=info
LOG_FILE_PATH=/var/log/digit-recognizer/app.log
```

## デプロイメント手順

### 1. 事前準備
```bash
# 依存関係インストール
cd server && npm ci --production
cd ../client && npm ci && npm run build

# Python依存関係
pip install -r ml/requirements.txt

# 環境設定
cp .env.example .env
# .env ファイルを適切に編集
```

### 2. セキュリティ確認
```bash
# 依存関係の脆弱性チェック
npm audit --audit-level=high
pip-audit

# ファイルパーミッション設定
chmod 600 .env
chmod 644 ml/svm_model.pkl
```

### 3. アプリケーション起動
```bash
# 本番モードでサーバー起動
NODE_ENV=production npm start

# プロセス管理 (PM2推奨)
pm2 start ecosystem.config.js
```

## 継続的セキュリティ

### 定期的なタスク
- [ ] 月次: 依存関係の脆弱性チェック
- [ ] 週次: セキュリティログの確認
- [ ] 日次: エラーログの監視
- [ ] 四半期: ペネトレーションテストの実施

### セキュリティ更新
- [ ] MLモデル更新時の整合性ハッシュ値更新
- [ ] APIキーの定期的なローテーション
- [ ] セキュリティパッチの適用

## 緊急時対応

### セキュリティインシデント発生時
1. アプリケーションの一時停止
2. ログの確保と分析
3. 影響範囲の特定
4. 修正パッチの適用
5. サービス復旧と監視強化

## 連絡先・サポート
- セキュリティ問題: security@your-domain.com
- 技術サポート: tech-support@your-domain.com
- インフラ管理: infra@your-domain.com