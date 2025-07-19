# macOS環境でのSSL証明書エラー トラブルシューティング

## 問題の概要

macOS環境でPython 3.13とscikit-learnを使用してMNISTデータセットを取得する際に、SSL証明書エラーが発生する問題です。

```
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate
```

## 影響する環境

- **OS**: macOS 15.x (Sequoia) 以降
- **Python**: 3.13.x
- **対象パッケージ**: scikit-learn, urllib, requests

## 自動修復方法（推奨）

### 1. SSL修復スクリプトの実行

```bash
npm run ssl-fix
```

このスクリプトは以下を自動実行します：
- SSL証明書の診断
- certifiライブラリのインストール・確認
- 環境変数の自動設定
- .envファイルへの設定保存

### 2. セットアップの再実行

```bash
npm run setup
```

## 手動修復方法

### 方法1: 環境変数の設定

```bash
# certifiライブラリのCA証明書バンドルを使用
export SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")
export REQUESTS_CA_BUNDLE=$(python3 -c "import certifi; print(certifi.where())")

# 設定を永続化
echo "export SSL_CERT_FILE=\$(python3 -c 'import certifi; print(certifi.where())')" >> ~/.zshrc
echo "export REQUESTS_CA_BUNDLE=\$(python3 -c 'import certifi; print(certifi.where())')" >> ~/.zshrc
```

### 方法2: Python証明書の更新

```bash
# Python証明書インストーラーを実行
/Applications/Python\ 3.13/Install\ Certificates.command
```

### 方法3: certifiライブラリの手動インストール

```bash
pip3 install --upgrade certifi
```

## .envファイルでの設定

プロジェクトの`.env`ファイルに以下を追加：

```env
# SSL証明書設定（macOS環境で必要な場合）
SSL_CERT_FILE=/path/to/certifi/cacert.pem
REQUESTS_CA_BUNDLE=/path/to/certifi/cacert.pem
```

証明書のパスは以下のコマンドで確認できます：

```bash
python3 -c "import certifi; print(certifi.where())"
```

## 診断コマンド

### SSL接続のテスト

```bash
python3 -c "
import ssl
import urllib.request
try:
    urllib.request.urlopen('https://api.openml.org', timeout=10)
    print('✅ SSL接続成功')
except Exception as e:
    print(f'❌ SSL接続失敗: {e}')
"
```

### 証明書パスの確認

```bash
python3 -c "
import certifi
import ssl
print(f'certifi CA bundle: {certifi.where()}')
print(f'Default CA bundle: {ssl.get_default_verify_paths().cafile}')
"
```

### システム情報の確認

```bash
# Python バージョン
python3 --version

# macOS バージョン
sw_vers -productVersion

# 環境変数の確認
echo "SSL_CERT_FILE: $SSL_CERT_FILE"
echo "REQUESTS_CA_BUNDLE: $REQUESTS_CA_BUNDLE"
```

## 最後の手段（非推奨）

**セキュリティリスクがあるため本番環境では使用しないでください。**

開発環境でのみ、一時的にSSL検証を無効化：

```python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

## 予防策

### 1. 仮想環境の使用

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r ml/requirements.txt
```

### 2. 定期的な証明書更新

```bash
# 月次実行を推奨
pip install --upgrade certifi
```

### 3. 環境設定の自動化

シェル設定ファイル（`.zshrc`、`.bash_profile`など）に環境変数を追加：

```bash
# SSL証明書設定
if command -v python3 &> /dev/null; then
    export SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())" 2>/dev/null || echo "")
    export REQUESTS_CA_BUNDLE=$SSL_CERT_FILE
fi
```

## トラブルシューティングのフローチャート

```
SSL証明書エラー発生
        ↓
npm run ssl-fix 実行
        ↓
エラー解決？ → YES → 完了
        ↓ NO
手動で環境変数設定
        ↓
エラー解決？ → YES → 完了
        ↓ NO
Python証明書更新実行
        ↓
エラー解決？ → YES → 完了
        ↓ NO
一時的SSL無効化（非推奨）
```

## 関連情報

- [Python SSL Documentation](https://docs.python.org/3/library/ssl.html)
- [certifi Library](https://pypi.org/project/certifi/)
- [scikit-learn データセット取得](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_openml.html)

## サポート

問題が解決しない場合は、以下の情報と共にIssueを作成してください：

1. macOSバージョン (`sw_vers -productVersion`)
2. Pythonバージョン (`python3 --version`)
3. エラーの完全なスタックトレース
4. 試行した解決策
5. 環境変数の現在の設定