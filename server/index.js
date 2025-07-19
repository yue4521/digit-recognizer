// 必要なモジュールをインポート
const express = require('express');      // Express Webフレームワーク
const cors = require('cors');            // CORS（Cross-Origin Resource Sharing）対応
const path = require('path');            // ファイルパス操作
require('dotenv').config({ path: path.join(__dirname, '..', '.env') }); // 環境変数の読み込み

// 予測API用のルートをインポート
const predictRoute = require('./routes/predict');

// 認証ミドルウェアをインポート
const { optionalAuth, securityHeaders } = require('./middleware/auth');

// Expressアプリケーションを初期化
const app = express();
// サーバーポートを設定（環境変数から取得、デフォルトは5000）
const PORT = process.env.PORT || 5000;

// ミドルウェアの設定
app.use(securityHeaders);                           // セキュリティヘッダーを設定
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
  credentials: true,
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type', 'x-api-key']
}));                                                // CORS設定を厳格化
app.use(express.json({ limit: '10mb' }));           // JSON形式のリクエストボディを解析（制限付き）
app.use(express.urlencoded({ extended: true, limit: '10mb' })); // URLエンコードされたデータを解析（制限付き）

// APIルートの設定
app.use('/api', predictRoute);  // /api 以下のルートを予測APIに委譲

// ヘルスチェック用エンドポイント（認証不要）
app.get('/api/health', optionalAuth, (req, res) => {
  res.json({ 
    status: 'サーバーが実行中です', 
    timestamp: new Date().toISOString(),
    authenticated: !!req.auth
  });
});

// セキュアなエラーハンドリングミドルウェア
app.use((error, req, res, next) => {
  // 詳細なエラーログを記録（内部のみ）
  console.error('エラー詳細:', {
    message: error.message,
    stack: error.stack,
    timestamp: new Date().toISOString(),
    ip: req.ip,
    url: req.url,
    method: req.method
  });
  
  // 本番環境では詳細なエラー情報を隠蔽
  const isDevelopment = process.env.NODE_ENV !== 'production';
  
  let statusCode = 500;
  let errorMessage = '内部サーバーエラーが発生しました';
  
  // 既知のエラータイプに基づく分類
  if (error.message.includes('セキュリティエラー')) {
    statusCode = 403;
    errorMessage = 'アクセスが拒否されました';
  } else if (error.message.includes('認証エラー')) {
    statusCode = 401;
    errorMessage = '認証が必要です';
  } else if (error.message.includes('ファイル')) {
    statusCode = 400;
    errorMessage = 'ファイル処理エラーです';
  } else if (error.message.includes('レート制限')) {
    statusCode = 429;
    errorMessage = 'リクエスト制限に達しました';
  }
  
  res.status(statusCode).json({
    error: 'リクエストの処理に失敗しました',
    message: errorMessage,
    // 開発環境でのみ詳細なエラー情報を提供
    ...(isDevelopment && { 
      details: error.message,
      timestamp: new Date().toISOString()
    })
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