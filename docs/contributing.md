# 貢献ガイド

手書き数字認識アプリへの貢献方法について説明します。

## 貢献の方法

### 1. リポジトリの準備

```bash
# リポジトリをフォーク
git clone <your-fork-url>
cd digit-recognizer

# 開発環境のセットアップ
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
npm run setup
```

### 2. 開発フロー

1. **機能ブランチを作成**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **変更を実装**
   - コーディングスタイルに従う
   - テストを追加・更新
   - ドキュメントを更新

3. **変更をコミット**
   ```bash
   git add .
   git commit -m "feat: 新機能の追加"
   ```

4. **プルリクエストを作成**
   - 明確なタイトルと説明
   - 変更内容の詳細説明
   - テスト結果の共有

## コーディングスタイル

### JavaScript/React
- ESLintルールに従う
- 関数型コンポーネントを使用
- PropTypesまたはTypeScriptで型定義

### Python
- PEP 8に従う
- docstringで関数を文書化
- type hintsの使用を推奨

### コミットメッセージ
Conventional Commitsに従う：
- `feat:` 新機能
- `fix:` バグ修正
- `docs:` ドキュメント変更
- `refactor:` リファクタリング

## テスト

### フロントエンド
```bash
cd client
npm test
```

### バックエンド
```bash
cd server
npm test
```

### 機械学習
```bash
cd ml
python -m pytest tests/
```

## 課題報告

バグや機能要求は以下の形式で報告してください：

### バグ報告
- 期待される動作
- 実際の動作
- 再現手順
- 環境情報（OS、ブラウザ等）

### 機能要求
- 機能の概要
- 使用ケース
- 実装案（あれば）

## ライセンス

このプロジェクトはMIT Licenseの下で公開されています。貢献することで、あなたの変更もMIT Licenseの下で公開されることに同意したものとみなされます。

## 謝辞

このプロジェクトの開発に貢献いただいている皆様に感謝します：

- **MNISTデータセット** - Yann LeCun
- **scikit-learn** - 機械学習ライブラリ
- **React** - UIライブラリ
- **Express.js** - Node.jsフレームワーク

## 連絡先

質問や提案がある場合は、GitHubのIssuesまたはDiscussionsをご利用ください。