#!/bin/bash
# macOS環境でのSSL証明書問題修復スクリプト

set -e

echo "🔧 macOS SSL証明書問題の診断・修復を開始します..."

# Python のバージョンチェック
PYTHON_VERSION=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
echo "📋 Python バージョン: $PYTHON_VERSION"

# OS情報の確認
OS_VERSION=$(sw_vers -productVersion)
echo "📋 macOS バージョン: $OS_VERSION"

# 現在の SSL 環境変数の確認
echo "📋 現在のSSL設定:"
echo "  SSL_CERT_FILE: ${SSL_CERT_FILE:-未設定}"
echo "  REQUESTS_CA_BUNDLE: ${REQUESTS_CA_BUNDLE:-未設定}"

# certifi ライブラリのインストール確認
echo "🔍 certifi ライブラリの確認..."
if python3 -c "import certifi; print(f'certifi location: {certifi.where()}')" 2>/dev/null; then
    CERTIFI_PATH=$(python3 -c "import certifi; print(certifi.where())")
    echo "✅ certifi が見つかりました: $CERTIFI_PATH"
else
    echo "❌ certifi が見つかりません。インストールを試行します..."
    pip3 install certifi
    CERTIFI_PATH=$(python3 -c "import certifi; print(certifi.where())")
    echo "✅ certifi をインストールしました: $CERTIFI_PATH"
fi

# SSL証明書のテスト
echo "🔍 SSL接続テスト..."
if python3 -c "
import ssl
import urllib.request
try:
    urllib.request.urlopen('https://api.openml.org', timeout=10)
    print('✅ SSL接続成功')
except Exception as e:
    print(f'❌ SSL接続失敗: {e}')
    exit(1)
" 2>/dev/null; then
    echo "✅ SSL証明書は正常に動作しています"
else
    echo "🔧 SSL証明書の修復を実行します..."
    
    # 環境変数の設定
    export SSL_CERT_FILE="$CERTIFI_PATH"
    export REQUESTS_CA_BUNDLE="$CERTIFI_PATH"
    
    echo "🔧 環境変数を設定しました:"
    echo "  SSL_CERT_FILE=$SSL_CERT_FILE"
    echo "  REQUESTS_CA_BUNDLE=$REQUESTS_CA_BUNDLE"
    
    # Python証明書インストールコマンドの実行（存在する場合）
    CERT_INSTALLER="/Applications/Python $PYTHON_VERSION/Install Certificates.command"
    if [ -f "$CERT_INSTALLER" ]; then
        echo "🔧 Python証明書インストーラーを実行します..."
        "$CERT_INSTALLER" || echo "⚠️  証明書インストーラーの実行に失敗しました"
    else
        echo "ℹ️  Python証明書インストーラーが見つかりません: $CERT_INSTALLER"
    fi
    
    # 再テスト
    echo "🔍 修復後のSSL接続テスト..."
    if SSL_CERT_FILE="$CERTIFI_PATH" REQUESTS_CA_BUNDLE="$CERTIFI_PATH" python3 -c "
import ssl
import urllib.request
import os
os.environ['SSL_CERT_FILE'] = '$CERTIFI_PATH'
os.environ['REQUESTS_CA_BUNDLE'] = '$CERTIFI_PATH'
try:
    urllib.request.urlopen('https://api.openml.org', timeout=10)
    print('✅ 修復後SSL接続成功')
except Exception as e:
    print(f'❌ 修復後もSSL接続失敗: {e}')
    exit(1)
"; then
        echo "✅ SSL証明書の修復が完了しました"
        
        # .env ファイルの更新
        if [ -f ".env" ]; then
            # 既存の SSL 設定を削除
            sed -i '' '/^SSL_CERT_FILE=/d' .env
            sed -i '' '/^REQUESTS_CA_BUNDLE=/d' .env
        else
            touch .env
        fi
        
        # 新しい SSL 設定を追加
        echo "SSL_CERT_FILE=$CERTIFI_PATH" >> .env
        echo "REQUESTS_CA_BUNDLE=$CERTIFI_PATH" >> .env
        
        echo "✅ .env ファイルにSSL設定を保存しました"
    else
        echo "❌ SSL証明書の修復に失敗しました"
        echo ""
        echo "💡 手動での対処方法:"
        echo "1. 次のコマンドを実行してください:"
        echo "   export SSL_CERT_FILE=\"$CERTIFI_PATH\""
        echo "   export REQUESTS_CA_BUNDLE=\"$CERTIFI_PATH\""
        echo ""
        echo "2. または、Python証明書を手動で更新してください:"
        echo "   \"$CERT_INSTALLER\""
        echo ""
        echo "3. 最後の手段として、SSL検証を一時的に無効化できます（非推奨）"
        exit 1
    fi
fi

echo ""
echo "🎉 SSL設定の診断・修復が完了しました！"
echo "ℹ️  npm run setup を再実行してください"