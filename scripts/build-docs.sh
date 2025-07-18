#!/bin/bash

# ドキュメント関連処理用スクリプト
# digit-recognizer プロジェクト用

set -e

echo "=== ドキュメント処理スクリプト ==="

# プロジェクトルートディレクトリの確認
if [ ! -f "package.json" ]; then
    echo "エラー: プロジェクトルートディレクトリで実行してください"
    exit 1
fi

# docsディレクトリの存在確認
if [ ! -d "docs" ]; then
    echo "docsディレクトリが見つかりません。作成します..."
    mkdir -p docs
fi

# ドキュメントファイルの存在確認
docs_files=(
    "docs/installation.md"
    "docs/api.md"
    "docs/architecture.md"
    "docs/development.md"
    "docs/ml-details.md"
    "docs/troubleshooting.md"
)

echo "ドキュメントファイルの確認中..."
missing_files=0

for file in "${docs_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "✗ $file (見つかりません)"
        missing_files=$((missing_files + 1))
    fi
done

if [ $missing_files -eq 0 ]; then
    echo "すべてのドキュメントファイルが存在します。"
else
    echo "警告: $missing_files 個のドキュメントファイルが見つかりません。"
fi

# READMEファイルの確認
if [ -f "README.md" ]; then
    echo "✓ README.md"
    # 絵文字の使用確認
    emoji_count=$(grep -o "[\U1F600-\U1F64F\U1F300-\U1F5FF\U1F680-\U1F6FF\U1F1E0-\U1F1FF\U2600-\U26FF\U2700-\U27BF]" README.md 2>/dev/null | wc -l || echo "0")
    if [ "$emoji_count" -gt 0 ]; then
        echo "警告: README.mdに絵文字が含まれています ($emoji_count 個)"
    else
        echo "✓ README.mdに絵文字は含まれていません"
    fi
else
    echo "✗ README.md (見つかりません)"
fi

# docsフォルダへのリンク確認
if [ -f "README.md" ]; then
    link_count=$(grep -c "docs/" README.md || echo "0")
    if [ "$link_count" -gt 0 ]; then
        echo "✓ README.mdにdocsフォルダへのリンクがあります ($link_count 個)"
    else
        echo "警告: README.mdにdocsフォルダへのリンクが見つかりません"
    fi
fi

echo ""
echo "=== ドキュメント処理完了 ==="

# オプション: Markdownファイルの構文チェック（markdownlintがインストールされている場合）
if command -v markdownlint >/dev/null 2>&1; then
    echo "Markdownlintによる構文チェックを実行中..."
    markdownlint README.md docs/*.md || echo "警告: Markdownlintでエラーが検出されました"
else
    echo "markdownlintが見つかりません。構文チェックをスキップします。"
fi

echo "ドキュメント処理スクリプト完了"