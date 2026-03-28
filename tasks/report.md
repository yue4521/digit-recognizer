# セキュリティ調査レポート

**作成日:** 2026-03-28
**対象リポジトリ:** digit-recognizer
**調査範囲:** GitHub Security Overview / GitHub Actions Security Audit

---

## 概要

| カテゴリ | 件数 | 最高深刻度 |
|----------|------|-----------|
| npm依存関係の脆弱性 (client/) | 20件 | High |
| GitHub Actionsの設定問題 | 6件 | Medium |
| サーバーコードの問題 | 2件 | Low/Medium |
| Python/Bandit | 0件 | - |

---

## 1. npm依存関係の脆弱性 (client/)

### 1-1. serialize-javascript — High (RCE / DoS)

| 項目 | 内容 |
|------|------|
| 影響パッケージ | `serialize-javascript <= 7.0.4` |
| 経路 | `react-scripts` → `css-minimizer-webpack-plugin` → `serialize-javascript` |
| GHSA | [GHSA-5c6j-r48x-rmvq](https://github.com/advisories/GHSA-5c6j-r48x-rmvq) / [GHSA-qj8w-gfj5-8c6v](https://github.com/advisories/GHSA-qj8w-gfj5-8c6v) |
| CWE | CWE-96 (RCE), CWE-400/CWE-834 (CPU消費によるDoS) |
| 説明 | `RegExp.flags` および `Date.prototype.toISOString()` を通じたコード実行。クラフトされた配列様オブジェクトによる無限ループ。 |
| 対応 | `react-scripts` の代替（Vite等）への移行が根本解決。`npm audit fix --force` は破壊的変更を伴うため要注意。 |

### 1-2. underscore — High (DoS)

| 項目 | 内容 |
|------|------|
| 影響パッケージ | `underscore <= 1.13.7` |
| GHSA | [GHSA-qpx9-hpmf-5gmw](https://github.com/advisories/GHSA-qpx9-hpmf-5gmw) |
| CWE | CWE-674 / CWE-770 (無制限再帰) |
| 説明 | `_.flatten` および `_.isEqual` が無制限再帰でDoSを引き起こす可能性。 |
| 対応 | `react-scripts` の更新待ちまたは移行。 |

### 1-3. webpack-dev-server — Moderate (ソースコード漏洩)

| 項目 | 内容 |
|------|------|
| 影響パッケージ | `webpack-dev-server <= 5.2.0` |
| GHSA | [GHSA-9jgg-88mc-972h](https://github.com/advisories/GHSA-9jgg-88mc-972h) / [GHSA-4v9v-hfq4-rm2v](https://github.com/advisories/GHSA-4v9v-hfq4-rm2v) |
| CWE | CWE-346 / CWE-749 |
| 説明 | 悪意あるWebサイトへアクセスすると開発サーバーのソースコードが窃取される可能性。 |
| 対応 | `client/package.json` の `overrides` で `4.15.2` に固定済み（緩和措置適用済み）。ただし `npm audit` 上は依然として表示される。 |

### 1-4. @tootallnate/once — Low

| 項目 | 内容 |
|------|------|
| 影響パッケージ | `@tootallnate/once < 3.0.1` |
| GHSA | [GHSA-vpq2-c234-7xj6](https://github.com/advisories/GHSA-vpq2-c234-7xj6) |
| CWE | CWE-705 (不正な制御フロー) |
| 対応 | `react-scripts` 経由の間接依存。`npm audit fix` で修正可能。 |

### 1-5. その他の高・中度脆弱性 (カスケード)

以下のパッケージは上記の脆弱性パッケージに依存することで高・中度に分類されている。

| パッケージ | 深刻度 | 原因 |
|-----------|--------|------|
| `bfj` (7.1.0 - 9.1.2) | High | `jsonpath` 経由 |
| `jsonpath` (all) | High | 直接的なアドバイザリ |
| `react-scripts` (>=0.1.0) | High | `css-minimizer-webpack-plugin` 経由 |
| `rollup-plugin-terser` | High | `serialize-javascript` 経由 |
| `workbox-build` (5.x - 7.x) | High | `serialize-javascript` 経由 |
| `workbox-webpack-plugin` (5.x - 7.x) | High | `serialize-javascript` 経由 |
| `@pmmmwh/react-refresh-webpack-plugin` | Moderate | `webpack-dev-server` 経由 |

**根本原因:** `react-scripts@5.x` (Create React App) が古いビルドツールチェーンを内包しており、メンテナンスが停止に近い状態。これらの脆弱性の大半はビルド時のみ影響し、**プロダクションバンドルには含まれない**。ただし開発環境のセキュリティリスクは実在する。

---

## 2. GitHub Actionsの設定問題

### 2-1. アクションがSHA固定されていない (Medium)

**対象ファイル:** `.github/workflows/ci.yml`, `security.yml`, `release.yml`

フローティングタグ（`@v4`, `@v5`）を使用しているため、アクションのメンテナが悪意あるコードをタグに上書きすると、次回実行時に自動的に取り込まれる（サプライチェーン攻撃リスク）。

```yaml
# 現状 (脆弱)
uses: actions/checkout@v4

# 推奨 (SHA固定)
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

**特に注意:** `getsentry/action-setup-venv@v2.2.0` はサードパーティ製アクションであり、SHA固定が特に重要。

### 2-2. TruffleHog Dockerイメージが `latest` タグ (Medium)

**対象ファイル:** `.github/workflows/security.yml` L135, L139

```yaml
docker run --rm -v "$PWD:/pwd" trufflesecurity/trufflehog:latest ...
```

`latest` タグはバージョン固定がなく、予期せぬ変更が取り込まれる可能性がある。特定バージョン（例: `v3.88.27`）への固定を推奨。

### 2-3. セキュリティチェックがすべて `continue-on-error: true` (Medium)

**対象ファイル:** `.github/workflows/security.yml` L64, L98, L103, L108, L170, L174

個別のセキュリティジョブ（`npm audit`, `safety`, `bandit`, `semgrep`等）がすべて `continue-on-error: true` であるため、脆弱性が検出されてもワークフロー自体は成功扱いとなる。`critical-vulnerabilities` ジョブが最終チェックとして機能しているが、アーティファクトのダウンロードに依存しており、個別ジョブの失敗時に正確に機能しない可能性がある。

### 2-4. release.yml でmainブランチへの直接プッシュ (Medium)

**対象ファイル:** `.github/workflows/release.yml` L50

```yaml
git push origin HEAD:main || echo "Push failed but continuing workflow"
```

GitHub Actionsのシステムトークンを使ってmainへ直接プッシュしており、ブランチ保護ルールをバイパスする可能性がある。また失敗しても `|| echo` でワークフローが継続するため、失敗が検知されにくい。

### 2-5. ci.yml の `push` トリガーにブランチフィルタなし (Low)

**対象ファイル:** `.github/workflows/ci.yml` L4

```yaml
on:
  push:   # ← 全ブランチへのpushで実行
  pull_request:
    branches: [main]
```

全ブランチへのpushでCIが実行されるため、Actions実行時間の無駄遣いやコスト増加につながる。セキュリティ上は低リスクだが、攻撃者がフォークからCIリソースを消費させるリスク（Actions abuse）がある。

### 2-6. ESLintとテストが無効化されたまま (Low)

**対象ファイル:** `.github/workflows/ci.yml` L27-31

```yaml
# - name: ESLint実行  # 一時的に無効化（ESLint v9設定の問題）
# - name: テスト実行  # 一時的に無効化（testスクリプトが定義されていない）
```

「一時的に無効化」されたまま放置されており、コード品質・セキュリティチェックが自動実行されていない。

---

## 3. サーバーコードの問題

### 3-1. CORSがすべてのオリジンを許可 (Medium)

**対象ファイル:** `server/index.js` L11

```js
app.use(cors());  // 全オリジン許可
```

CORS設定が無制限であり、任意のオリジンからAPIへのアクセスが可能。本番環境では `origin` オプションで許可するオリジンを制限すべき。

### 3-2. ファイルタイプ検証がMIMEタイプのみ (Low)

**対象ファイル:** `server/routes/predict.js` L34-41

```js
const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
if (allowedTypes.includes(file.mimetype)) { ... }
```

MIMEタイプはリクエストヘッダで偽装可能。マジックバイト（ファイルシグネチャ）の検証を行っていないため、拡張子偽装されたファイルがアップロードされる可能性がある。ただし `multer` のファイルサイズ制限（2MB）は適用されており、ファイルパス検証（`path.relative` によるディレクトリトラバーサル対策）も実装済み。

---

## 4. Bandit (Python静的解析)

`ml/` 以下のPythonコード（770行）に対してBanditを実行した結果、**問題は検出されなかった**。

---

## 5. Dependabotの設定について

`client/` の `dependabot.yml` で以下のバージョンが意図的に無視されている：

```yaml
ignore:
  - dependency-name: "nth-check"
    versions: ["< 2.0.1"]
  - dependency-name: "postcss"
    versions: ["< 8.4.31"]
  - dependency-name: "webpack-dev-server"
    versions: ["<= 5.2.0"]
```

これらは `react-scripts` の間接依存であり、現状 `overrides` で緩和措置が取られている。Dependabotが不要なPRを生成しないよう適切に設定されている。

---

## 推奨対応 (優先度順)

| 優先度 | 項目 | 対応方針 |
|--------|------|----------|
| 高 | client/ npm脆弱性 (serialize-javascript等) | `react-scripts` からViteへの移行を中長期計画として検討。短期はビルド環境のみに限定し本番への影響を把握する。 |
| 中 | GitHub ActionsのSHA固定 | 主要アクション（`actions/checkout`, `actions/setup-node`等）を特定SHAに固定。 |
| 中 | TruffleHog `latest` → 特定バージョン固定 | `trufflesecurity/trufflehog:v3.88.27` 等の固定タグを使用。 |
| 中 | release.ymlの直接プッシュ見直し | mainへの直接プッシュ方式の見直し。ブランチ保護ルールとの整合性を確認。 |
| 低 | CORS設定の制限 | 本番環境では許可オリジンを明示的に指定。 |
| 低 | ESLint/テストの再有効化 | ESLint v9設定を修正し、CIチェックを復活させる。 |

---

## 参考: npm audit 集計 (2026-03-28時点)

| ディレクトリ | Critical | High | Moderate | Low |
|-------------|----------|------|----------|-----|
| root (`/`) | 0 | 0 | 0 | 0 |
| `client/` | 0 | 9 | 2 | 9 |
| `server/` | 0 | 0 | 0 | 0 |
