// 必要なモジュールをインポート
const express = require('express');      // Express Webフレームワーク
const cors = require('cors');            // CORS（Cross-Origin Resource Sharing）対応
const path = require('path');            // ファイルパス操作
require('dotenv').config();              // 環境変数の読み込み

// 予測API用のルートをインポート
const predictRoute = require('./routes/predict');

// Expressアプリケーションを初期化
const app = express();
// サーバーポートを設定（環境変数から取得、デフォルトは5000）
const PORT = process.env.PORT || 5000;

// ミドルウェアの設定
app.use(cors());                                    // CORS設定を有効化
app.use(express.json());                            // JSON形式のリクエストボディを解析
app.use(express.urlencoded({ extended: true }));    // URLエンコードされたデータを解析

// APIルートの設定
app.use('/api', predictRoute);  // /api 以下のルートを予測APIに委譲

// ヘルスチェック用エンドポイント
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'サーバーが実行中です', 
    timestamp: new Date().toISOString() 
  });
});

// エラーハンドリングミドルウェア
app.use((error, req, res, next) => {
  console.error('エラー:', error.message);
  res.status(500).json({
    error: '内部サーバーエラー',
    message: error.message
  });
});

// 404エラーハンドラー
app.use('*', (req, res) => {
  res.status(404).json({
    error: '見つかりません',
    message: '要求されたリソースが見つかりませんでした'
  });
});

// サーバーを開始
app.listen(PORT, () => {
  console.log(`サーバーがポート ${PORT} で実行中`);
  console.log(`ヘルスチェック: http://localhost:${PORT}/api/health`);
});