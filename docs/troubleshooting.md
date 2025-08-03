# トラブルシューティング

## よくある問題と解決方法

### インストール関連

#### 「モジュールが見つかりません」エラー

**症状**: `Module not found`や`Cannot find module`エラー

**解決方法**:
```bash
# 全ての依存関係を再インストール
npm run install-all

# 個別にインストール
cd client && npm install
cd ../server && npm install
```

#### Python依存関係のエラー

**症状**: `ModuleNotFoundError: No module named 'sklearn'`

**解決方法**:
```bash
# 仮想環境がアクティブか確認
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Python依存関係を再インストール
pip install -r ml/requirements.txt
```

#### 仮想環境が作成できない

**症状**: `python3 -m venv venv`が失敗

**解決方法**:
```bash
# Pythonのバージョン確認
python3 --version

# python3-venvをインストール (Ubuntu/Debian)
sudo apt-get install python3-venv

# Homebrewでpyenvを使用 (macOS)
brew install pyenv
```

### モデル関連

#### モデルファイルが見つからない

**症状**: `FileNotFoundError: svm_model.pkl`

**解決方法**:
```bash
# モデルを再訓練
npm run train-model

# 手動でモデル訓練
cd ml
python3 train_model.py
```

#### モデル訓練が失敗する

**症状**: MNISTデータセットのダウンロードエラー

**解決方法**:
```bash
# インターネット接続を確認
# 仮想環境内でscikit-learnが正しくインストールされているか確認
pip list | grep scikit

# 必要に応じて再インストール
pip install --upgrade scikit-learn
```

### サーバー関連

#### ポートが既に使用中

**症状**: `Error: listen EADDRINUSE :::3000`や`:::5000`

**解決方法**:
```bash
# 使用中のプロセスを確認
lsof -i :3000
lsof -i :5000

# プロセスを終了
kill -9 <PID>

# または.envでポートを変更
echo "PORT=5001" >> .env
```

#### CORS エラー

**症状**: ブラウザで`Access to fetch at ... has been blocked by CORS policy`

**解決方法**:
- `server/index.js`のCORS設定を確認
- フロントエンドとバックエンドのポート設定を確認
- 必要に応じて CORS設定を更新

### 予測関連

#### 画像アップロードが失敗

**症状**: `400 Bad Request`や「ファイルがアップロードされていません」

**解決方法**:
- ファイル形式がJPEGまたはPNGか確認
- ファイルサイズが2MB以下か確認
- ブラウザのネットワークタブでリクエストを確認

#### 予測精度が低い

**症状**: 明らかに正しい数字を間違って認識

**解決方法**:
- 画像の背景色を確認（白背景に黒文字、または黒背景に白文字）
- 画像にノイズが多くないか確認
- 数字が画像の中央に配置されているか確認
- 複数の数字が含まれていないか確認

#### Pythonスクリプトがタイムアウト

**症状**: `Python script execution timeout`

**解決方法**:
- 画像ファイルサイズを確認
- Python環境のメモリ使用量を確認
- スクリプトのタイムアウト設定を調整

### プラットフォーム固有の問題

#### Windows環境

**問題**: PowerShellでの仮想環境アクティベーション失敗

**解決方法**:
```powershell
# 実行ポリシーを変更
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 仮想環境をアクティベート
venv\Scripts\Activate.ps1
```

**問題**: Pythonコマンドが見つからない

**解決方法**:
- Python公式サイトからインストール
- 環境変数PATHにPythonを追加
- `python`コマンドの代わりに`py`を使用

#### macOS環境

**問題**: `xcrun: error: invalid active developer path`

**解決方法**:
```bash
# Xcode Command Line Toolsをインストール
xcode-select --install
```

**問題**: Homebrewのパッケージ競合

**解決方法**:
```bash
# Homebrewを更新
brew update && brew upgrade

# 必要に応じてPythonを再インストール
brew reinstall python@3.9
```

#### Linux環境

**問題**: Python開発ヘッダーがない

**解決方法**:
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev

# CentOS/RHEL
sudo yum install python3-devel
```

## ログとデバッグ

### フロントエンドのデバッグ

1. ブラウザのDevToolsを開く
2. Consoleタブでエラーメッセージを確認
3. Networkタブでリクエスト/レスポンスを確認

### バックエンドのデバッグ

1. サーバーのコンソール出力を確認
2. `console.log`でデバッグ情報を追加
3. API テストツール（Postman等）で直接テスト

### Python処理のデバッグ

1. `ml/predict.py`にprint文を追加
2. 画像前処理の各段階を確認
3. モデルの出力を詳細に検証

## パフォーマンスの問題

### 予測が遅い

**症状**: 予測に5秒以上かかる

**確認事項**:
- 画像サイズが適切か
- 仮想環境内でライブラリが正しくインストールされているか
- システムリソース（CPU/メモリ）に問題がないか

### メモリ使用量が多い

**症状**: システムが重くなる

**対策**:
- 不要な開発サーバーを停止
- ブラウザのタブを整理
- 大きな画像ファイルの使用を避ける

## サポートとヘルプ

問題が解決しない場合：

1. プロジェクトのREADME.mdを再確認
2. 各コンポーネントのログを詳細に確認
3. 開発者ガイドの手順を再実行
4. 必要に応じて環境をクリーンインストール