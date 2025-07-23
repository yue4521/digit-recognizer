# GitHub Actions CI/CDガイド

## GitHub Actionsとは

GitHub Actionsは、GitHubが提供する無料のCI/CD（継続的インテグレーション/継続的デプロイメント）サービスです。コードをGitHubにpushするだけで、自動的にテスト、ビルド、デプロイなどが実行されます。

### 新人エンジニアにとってのメリット

1. **自動化された品質管理** - 手動でのテスト実行忘れを防止
2. **学習効果** - コードの問題点を自動で教えてくれる
3. **チーム開発の効率化** - プルリクエスト時の自動チェック
4. **安心してデプロイ** - 問題のあるコードが本番に行くのを防止

## 本プロジェクトのワークフロー構成

手書き数字認識アプリに以下の5つのワークフローが導入されています：

### 1. CI（ci.yml）- メインCI/CDパイプライン

**実行タイミング**: push時とプルリクエスト時
**目的**: 包括的な品質チェックとビルド確認

```yaml
トリガー: main・taskブランチへのpush、mainへのPR
実行内容:
- Node.js (18.x, 20.x) × Python (3.8, 3.9, 3.10) のマトリックステスト
- 依存関係インストール
- JavaScript/TypeScript linting
- コードフォーマット確認
- Python linting
- アプリケーションビルド
- 機械学習モデル訓練テスト
```

### 2. Lint and Format（lint-and-format.yml）- 軽量品質チェック

**実行タイミング**: push時とプルリクエスト時
**目的**: 高速なコードスタイルチェック

```yaml
JavaScript/TypeScript Job:
- ESLint実行
- Prettierフォーマット確認

Python Job:
- flake8 linting
- black・isortフォーマット確認
```

### 3. Test Suite（test.yml）- 詳細テストスイート

**実行タイミング**: push時とプルリクエスト時
**目的**: 包括的なテスト実行とインテグレーション確認

```yaml
フロントエンドテスト:
- React テスト実行（利用可能な場合）
- フロントエンドビルド確認

バックエンドテスト:
- Express.js テスト実行（利用可能な場合）
- サーバー起動確認

インテグレーションテスト:
- 全体ビルド確認
- モデル訓練実行
- モデルファイル生成確認
```

### 4. Python Quality Checks（python-quality.yml）- Python品質チェック

**実行タイミング**: ml/フォルダ変更時
**目的**: Python/機械学習コードの品質とパフォーマンス確認

```yaml
実行内容:
- Python 3.8-3.11での動作確認
- flake8による静的解析
- black・isortによるフォーマット確認
- mypy型チェック（設定されている場合）
- pytest実行（テストがある場合）
- モデル訓練・予測テスト
```

### 5. Security Scan（security.yml）- セキュリティスキャン

**実行タイミング**: push・PR時、毎週日曜2:00AM（UTC）
**目的**: セキュリティ脆弱性の検出と予防

```yaml
依存関係スキャン:
- npm audit（高リスク以上）
- Python safety check
- bandit セキュリティスキャン

秘密情報検出:
- ハードコードされたAPIキー検出
- パスワード・トークン検出
- 機密情報パターンマッチング

コード品質・セキュリティ解析:
- ESLintセキュリティルール
- 危険なコードパターン検出
- システムレベルimport確認
```

## ワークフローの実行確認方法

### 1. GitHub上で確認

```
リポジトリ → Actions タブ → 実行結果確認
- 緑色のチェック: 成功
- 赤色のX: 失敗
- 黄色の円: 実行中
```

### 2. ローカルでの事前確認

実際にGitHubに push する前に、以下のコマンドでローカル確認可能：

```bash
# JavaScript/TypeScript linting
npm run lint

# コードフォーマット確認
npm run format:check

# Python linting
npm run lint:python

# アプリケーションビルド
npm run build

# モデル訓練
npm run train-model
```

## 新機能を追加する際のワークフロー

### 1. 機能開発時
```bash
# ブランチ作成
git checkout -b feature/新機能名

# 開発・テスト
npm run lint
npm run build

# コミット・プッシュ
git add .
git commit -m "feat: 新機能の実装"
git push origin feature/新機能名
```

### 2. プルリクエスト作成時
- GitHub上でPR作成
- 自動的に以下が実行される：
  - Lint and Format（約2-3分）
  - CI（約5-10分）
  - Test Suite（約3-5分）
  - Python Quality Checks（ml/変更時）
  - Security Scan（約5-7分）

### 3. 問題があった場合
```bash
# エラーログを確認し、ローカルで修正
npm run lint:fix  # 自動修正可能な問題を修正
git add .
git commit -m "fix: lintエラーを修正"
git push origin feature/新機能名
```

## トラブルシューティング

### よくあるエラーと解決方法

#### 1. Linting エラー
```bash
# エラー確認
npm run lint

# 自動修正
npm run lint:fix

# Python linting エラー
cd ml && flake8 .
cd ml && black . && isort .
```

#### 2. ビルドエラー
```bash
# 依存関係の再インストール
npm run install-all

# Python依存関係の再インストール
pip install -r ml/requirements.txt
```

#### 3. テストエラー
```bash
# 個別にテスト実行
cd client && npm test
cd server && npm test（テストがある場合）
```

#### 4. セキュリティエラー
```bash
# 依存関係の脆弱性確認
npm audit
npm audit fix

# Python脆弱性確認
cd ml && safety check
```

## ワークフローのカスタマイズ

### Node.jsバージョンの変更
```yaml
# .github/workflows/ci.yml
strategy:
  matrix:
    node-version: [18.x, 20.x, 22.x]  # バージョン追加
```

### Pythonバージョンの変更
```yaml
# .github/workflows/python-quality.yml
strategy:
  matrix:
    python-version: [3.8, 3.9, '3.10', '3.11', '3.12']
```

### 新しいワークフローの追加
```yaml
# .github/workflows/custom.yml
name: Custom Workflow
on:
  push:
    branches: [main]
jobs:
  custom-job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Custom Step
        run: echo "カスタム処理"
```

## パフォーマンス最適化

### 1. キャッシュの活用
```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

### 2. 並列実行の最適化
```yaml
jobs:
  job1:
    runs-on: ubuntu-latest
  job2:
    needs: job1  # job1完了後に実行
  job3:
    runs-on: ubuntu-latest  # job1と並列実行
```

## セキュリティベストプラクティス

### 1. シークレット管理
```yaml
# GitHub Settings > Secrets に設定
env:
  API_KEY: ${{ secrets.API_KEY }}
```

### 2. 権限の最小化
```yaml
permissions:
  contents: read
  pull-requests: write
```

### 3. 信頼できるActionの使用
```yaml
# 公式またはverified publisherのActionを使用
- uses: actions/checkout@v4  # 公式
- uses: actions/setup-node@v4  # 公式
```

## 継続的改善のポイント

1. **実行時間の監視** - 長すぎるワークフローは開発効率を下げる
2. **失敗率の確認** - 頻繁に失敗するチェックは設定見直しが必要
3. **コスト監視** - GitHubの使用制限を確認
4. **定期的な更新** - Action・依存関係のバージョン更新

## 関連ドキュメント

- [development.md](development.md) - 開発環境とプロセス
- [troubleshooting.md](troubleshooting.md) - 問題解決ガイド
- [production-deployment.md](production-deployment.md) - 本番環境配置