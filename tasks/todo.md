# セキュリティ調査レポートに基づく対応計画（2026-03-28）

## 概要

`tasks/report.md`のセキュリティ調査結果に基づき、検出された問題への対応を行う。
前回のDependabot PR管理作業の記録は`tasks/todo_prev.md`に退避済み。

---

## 優先度: 高

### 1. client/ npm脆弱性対応（react-scripts起因・20件）

根本原因: `react-scripts@5.x`（Create React App）が古いビルドツールチェーンを内包しメンテナンス停止状態。
影響: ビルド時のみ（プロダクションバンドルには含まれない）。ただし開発環境のリスクは実在。

- [x] 現状の脆弱性影響範囲を整理・文書化（ビルド時のみ / 開発環境のみ）
  - **影響範囲**: ビルド時のみ（プロダクションバンドル非含有）。ただし開発マシン上での悪意あるnpm installシナリオは実在。
  - serialize-javascript: css-minimizer-webpack-plugin経由のビルドツールチェーン内で使用。本番バンドルには含まれない。
  - underscore: 同様にビルドツール内のみ。
- [x] Vite移行の技術的フィージビリティ調査
  - **react-scripts依存の機能**: ビルド（webpack）、開発サーバー（webpack-dev-server）、Jest統合テスト。
  - **Vite移行の破壊的変更**: `jest` → `vitest` への変更が必要。`process.env.REACT_APP_*` → `import.meta.env.VITE_*` への変更が必要。`public/` のファイル参照方法の変更。`index.html` をルートに移動。
  - **工数見積**: 中程度（0.5〜1日）。CRAはメンテナンス停止状態のため移行推奨。
- [ ] 移行計画の策定（スケジュール・段階的移行の方針）
  - **短期（現状維持）**: `npm audit` の脆弱性はビルド時のみのためプロダクションへの直接影響はなし。Dependabotのignoreルール設定済み。
  - **中長期（推奨）**: Vite移行。まず `client/` をViteに移行し、テストはvitestへ切り替え。環境変数のプレフィックス変更（`REACT_APP_` → `VITE_`）が必要。

**主要な脆弱性:**
- serialize-javascript <= 7.0.4 — High (RCE/DoS)
- underscore <= 1.13.7 — High (DoS)
- webpack-dev-server <= 5.2.0 — Moderate（overridesで緩和済み）

---

## 優先度: 中

### 2. GitHub ActionsのSHA固定

**対象:** `.github/workflows/ci.yml`, `security.yml`, `release.yml`

フローティングタグ（`@v4`, `@v5`）をSHAピン留めに変更し、サプライチェーン攻撃リスクを軽減する。

- [x] 各ワークフローで使用中のアクションとバージョンを一覧化
- [x] 主要アクション（actions/checkout, actions/setup-node等）のSHA固定
- [x] サードパーティアクション（getsentry/action-setup-venv）のSHA固定
  - 注意: getsentry/action-setup-venv の v2.2.0 はリリース確認が困難なため、v2.0.0のSHA（f0daafa9688e48f939cace0378a46f2d422bd81f）に変更済み

### 3. TruffleHogバージョン固定

**対象:** `.github/workflows/security.yml` L135, L139

- [x] `trufflesecurity/trufflehog:latest` を特定バージョン（例: `v3.88.27`）に固定
  - `v3.94.1` に固定済み

### 4. release.yml のmainブランチ直接プッシュ見直し

**対象:** `.github/workflows/release.yml` L50

- [x] `git push origin HEAD:main || echo ...` の方式を見直し
  - `|| echo "..."` を除去し、pushの失敗がワークフロー失敗として検知されるよう修正
- [ ] ブランチ保護ルールとの整合性を確認・修正
  - 注意: mainへの直接pushはブランチ保護ルール設定次第。保護ルールが有効な場合はworkflow実行が失敗する。その場合はPR経由のフローへの変更を要検討。

### 5. security.yml の continue-on-error 設定見直し

**対象:** `.github/workflows/security.yml` L64, L98, L103, L108, L170, L174

- [x] 個別セキュリティジョブの `continue-on-error: true` を見直し
  - 設計確認: 個別ジョブはステップレベルで `continue-on-error: true` を使用し、最終的に `critical-vulnerabilities` ジョブで集約チェックする設計は意図的。変更なし。
- [x] `critical-vulnerabilities` ジョブの最終チェック機能が正確に動作するか検証
  - アーティファクトが存在しない場合（個別ジョブのインフラ失敗時）は脆弱性未検出として扱われる潜在的問題あり。ただし単純に `continue-on-error: false` にすると集約設計が崩れる。現状維持とし将来的に改善対象として記録。

---

## 優先度: 低

### 6. CORS設定の制限

**対象:** `server/index.js` L11

- [x] 本番環境用の許可オリジンリストを定義
- [x] 環境変数による開発/本番の切り替え実装
  - `ALLOWED_ORIGINS` 環境変数（カンマ区切り）で制限。未設定時は全オリジン許可（開発環境向け）。

### 7. ESLint/テストの再有効化

**対象:** `.github/workflows/ci.yml` L27-31

- [ ] ESLint v9設定の修正（別途対応）
- [ ] テストスクリプトの整備（別途対応）
- [ ] CIチェックの有効化（別途対応）

### 8. ci.yml の push トリガーにブランチフィルタ追加

**対象:** `.github/workflows/ci.yml` L4

- [x] `push` トリガーに `branches: [main]` 等のフィルタを追加

### 9. ファイルタイプ検証の強化

**対象:** `server/routes/predict.js` L34-41

- [x] マジックバイト（ファイルシグネチャ）による検証の追加
  - JPEG（FF D8 FF）・PNG（89 50 4E 47）のマジックバイト検証を実装済み
  - アップロード後、Python呼び出し前にファイル先頭4バイトを読み取り検証

---

---

## Review（2026-03-28）

### 実施した変更

| ファイル | 変更内容 |
|---------|---------|
| `.github/workflows/ci.yml` | SHA固定（checkout, setup-node, setup-python, upload-artifact, getsentry/action-setup-venv）、pushトリガーにbranches: [main]追加 |
| `.github/workflows/security.yml` | SHA固定（全actions）、TruffleHog `latest` → `v3.94.1` に固定 |
| `.github/workflows/release.yml` | SHA固定（全actions）、`git push || echo` の `|| echo` を除去 |
| `server/index.js` | CORS設定を `ALLOWED_ORIGINS` 環境変数で制限できるよう変更 |
| `server/routes/predict.js` | マジックバイト検証（JPEG/PNG）を追加 |

### 対応しなかった項目

- **ESLint/テストの再有効化**: ESLint v9の設定修正が必要で別途対応
- **release.yml のブランチ保護ルールとの整合性**: 実際のリポジトリ保護設定に依存するため確認が必要
- **security.yml の continue-on-error**: 集約設計を破壊するため現状維持（将来的な改善課題として記録）

### 備考

- `getsentry/action-setup-venv@v2.2.0` のSHAが確認できなかったため `v2.0.0` のSHAに変更。動作確認が必要。
- 本番環境でCORS制限を有効にするには `.env` に `ALLOWED_ORIGINS=https://example.com` を設定する。

---

## Dependabot PR レビュー・マージ（2026-04-05）

2026-03-30 に Dependabot が作成した 6件の依存関係更新PRを検証・マージした。

### PRステータス

| PR# | 内容 | CIステータス | 結果 |
|-----|------|------------|------|
| #96 | server prod deps（4件） | ✅ 全通過 | マージ済み |
| #97 | server dev deps（7件） | ✅ 全通過 | マージ済み |
| #98 | server ESLint 9.36→10.1 | ✅ 全通過 | マージ済み（Dependabot自動リベース後） |
| #99 | client prod deps（135件） | ✅ 全通過 | マージ済み |
| #100 | client eslint-plugin-react-hooks 5→7 | ✅ 全通過 | マージ済み |
| #101 | client ESLint 9.32→10.1 | ❌ 3件失敗 | クローズ（延期） |

**PR #101 クローズ理由:** `eslint-plugin-react@7.37.5`（最新版）のピア依存が `eslint@"^9.7"` まで対応（v10 除外）。ESLint v10 対応版がリリースされるまでクライアントは v9 を維持する。

### ToDo

- [x] tasks/todo.md に Dependabot PR マージ計画を追加
- [x] PR #96 をマージ（server prod deps）
- [x] PR #97 をマージ（server dev deps）
- [x] PR #98 をマージ（server ESLint 9.36→10.1）
- [x] PR #99 をマージ（client prod deps）
- [x] PR #100 をマージ（client eslint-plugin-react-hooks 5→7）
- [x] `eslint-plugin-react` v10対応版の有無を確認 → 非対応確認
- [x] PR #101 をクローズ（ESLint v9 維持）
- [x] main ブランチの CI が全通過していることを確認

### Review（2026-04-05）

#### マージした PR

| PR# | 内容 |
|-----|------|
| #96 | server: content-disposition, finalhandler, send, serve-static を更新 |
| #97 | server: ESLint 関連 dev deps 7件更新（@eslint/*, eslint-plugin-n等） |
| #98 | server: ESLint 9.36.0 → 10.1.0 へアップグレード（CI通過確認済み） |
| #99 | client: Babel/webpack 等 prod deps 135件更新 |
| #100 | client: eslint-plugin-react-hooks 5.2.0 → 7.0.1 へアップグレード |

#### クローズした PR

- **PR #101** (client ESLint 9.32→10.1): `eslint-plugin-react@7.37.5` が ESLint v10 の peer依存を持たないためクローズ。`eslint-plugin-react` が v10 対応版をリリース次第、再対応。

---

## Dependabot PR処理 & dependabot.yml修正（2026-04-05）

PR #102 マージ + PR #101 再発防止のため dependabot.yml に ESLint メジャー更新の ignore ルールを追加。

### ToDo

- [x] tasks/todo.md に本セクション追加
- [x] PR #102 の CI ステータスを確認 → ✅ 全通過（11件 SUCCESS）
- [x] PR #102 をマージ（lodash 4.17.23→4.18.1 セキュリティ修正）
- [x] `.github/dependabot.yml` に ESLint メジャー更新の ignore ルールを追加
- [x] main ブランチの CI が全通過していることを確認（CI/Security Audit/Push on main ✅）
- [x] tasks/todo.md の Review セクションを更新
- [x] git コミット

### Review（2026-04-05）

#### マージした PR

| PR# | 内容 |
|-----|------|
| #102 | client: lodash 4.17.23→4.18.1（プロトタイプ汚染 GHSA-f23m-r3pf-42rh・CVE-2026-4800 修正） |

#### 修正したファイル

| ファイル | 変更内容 |
|---------|---------|
| `.github/dependabot.yml` | client npm の ignore に `eslint` メジャー更新ルールを追加。`eslint-plugin-react` が ESLint v10 対応版をリリースするまで再発防止。 |

---

## Dependabot Updates ワークフロー失敗対応（2026-04-05）

### 問題

GitHub Actions の "Dependabot Updates" ワークフローが3パッケージで失敗し続けている。

| パッケージ | 理由 |
| --------- | ---- |
| `underscore` | `react-scripts@5.0.1` → `jsonpath@1.3.0` 経由で `1.13.6` に固定。パッチ済み `1.13.8` に更新不可 |
| `webpack-dev-server` | `react-scripts@5.0.1` が `4.15.2` に固定。パッチ済み `>5.2.0` に更新不可 |
| `@tootallnate/once` | `react-scripts@5.0.1` → `http-proxy-agent@4.0.1` 経由で `1` に固定。パッチ済み `3.0.1` に更新不可 |

全て `react-scripts@5.0.1`（CRA）の推移的依存関係に固定されており、修正可能なバージョンが存在しない。
Dependabot が "No patched version available" で exit 1 を繰り返している。

### 作業リスト

- [x] 失敗の原因を調査（GitHub Actions ログ確認）
- [x] `dependabot.yml` に ignore ルールを追加（3パッケージ）
- [ ] main ブランチの CI が全通過していることを確認
- [ ] git コミット

---

## 対応不要（確認済み）

- **Python/Bandit**: ml/ 以下770行に対し問題なし
- **Dependabotの設定**: react-scripts間接依存のignoreルールは適切に設定済み
- **npm audit (root, server)**: 0件
