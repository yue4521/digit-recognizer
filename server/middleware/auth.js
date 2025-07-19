/**
 * 認証ミドルウェア
 * 
 * セキュリティ機能：
 * - API キー認証
 * - レート制限（簡易版）
 * - 不正アクセス検出
 */

const crypto = require('crypto');

// 設定値
const AUTH_CONFIG = {
  // 開発用APIキー（本番環境では環境変数から取得）
  API_KEYS: [
    process.env.API_KEY || 'dev-api-key-12345',
    // 複数のAPIキーに対応可能
  ],
  // レート制限設定
  RATE_LIMIT: {
    WINDOW_MS: 15 * 60 * 1000, // 15分
    MAX_REQUESTS: 100 // 15分間に100リクエスト
  }
};

// レート制限用のメモリストア（本番環境ではRedisを推奨）
const rateLimitStore = new Map();

/**
 * APIキー認証ミドルウェア（開発環境でのバイパス機能付き）
 */
function authenticateAPIKey(req, res, next) {
  try {
    // 開発環境での認証バイパスチェック
    if (process.env.NODE_ENV === 'development' && process.env.DISABLE_AUTH === 'true') {
      console.log(`開発環境: 認証をバイパス - ${req.ip} - ${new Date().toISOString()}`);
      req.auth = {
        apiKey: 'dev-bypass',
        timestamp: new Date(),
        bypassed: true
      };
      return next();
    }
    
    // APIキーを取得（ヘッダーまたはクエリパラメータから）
    const apiKey = req.headers['x-api-key'] || req.query.api_key;
    
    if (!apiKey) {
      return res.status(401).json({
        error: '認証エラー',
        message: 'APIキーが必要です'
      });
    }
    
    // APIキーの検証
    if (!AUTH_CONFIG.API_KEYS.includes(apiKey)) {
      console.log(`不正なAPIキーでのアクセス試行: ${req.ip} - キー: ${apiKey.substring(0, 8)}...`);
      return res.status(403).json({
        error: '認証エラー',
        message: '無効なAPIキーです'
      });
    }
    
    // リクエストにユーザー情報を追加
    req.auth = {
      apiKey: apiKey,
      timestamp: new Date()
    };
    
    console.log(`認証成功: ${req.ip} - ${new Date().toISOString()}`);
    next();
    
  } catch (error) {
    console.error('認証エラー:', error.message);
    res.status(500).json({
      error: '内部エラー',
      message: '認証処理中にエラーが発生しました'
    });
  }
}

/**
 * 簡易レート制限ミドルウェア
 */
function rateLimit(req, res, next) {
  try {
    const clientId = req.ip + (req.auth?.apiKey || 'anonymous');
    const now = Date.now();
    
    // クライアントのリクエスト履歴を取得
    if (!rateLimitStore.has(clientId)) {
      rateLimitStore.set(clientId, []);
    }
    
    const requests = rateLimitStore.get(clientId);
    
    // 時間窓外のリクエストを削除
    const validRequests = requests.filter(
      timestamp => now - timestamp < AUTH_CONFIG.RATE_LIMIT.WINDOW_MS
    );
    
    // 制限チェック
    if (validRequests.length >= AUTH_CONFIG.RATE_LIMIT.MAX_REQUESTS) {
      console.log(`レート制限に達しました: ${clientId}`);
      return res.status(429).json({
        error: 'レート制限',
        message: '短時間に大量のリクエストが検出されました。しばらく待ってから再試行してください。',
        retryAfter: Math.ceil(AUTH_CONFIG.RATE_LIMIT.WINDOW_MS / 1000)
      });
    }
    
    // 現在のリクエストを記録
    validRequests.push(now);
    rateLimitStore.set(clientId, validRequests);
    
    // レスポンスヘッダーに制限情報を追加
    res.setHeader('X-RateLimit-Limit', AUTH_CONFIG.RATE_LIMIT.MAX_REQUESTS);
    res.setHeader('X-RateLimit-Remaining', AUTH_CONFIG.RATE_LIMIT.MAX_REQUESTS - validRequests.length);
    res.setHeader('X-RateLimit-Reset', new Date(now + AUTH_CONFIG.RATE_LIMIT.WINDOW_MS).toISOString());
    
    next();
    
  } catch (error) {
    console.error('レート制限エラー:', error.message);
    next(); // レート制限エラーは通す
  }
}

/**
 * 認証不要のエンドポイント用ミドルウェア
 * （ヘルスチェック等）
 */
function optionalAuth(req, res, next) {
  // APIキーがあれば認証、なければそのまま通す
  const apiKey = req.headers['x-api-key'] || req.query.api_key;
  
  if (apiKey) {
    return authenticateAPIKey(req, res, next);
  }
  
  next();
}

/**
 * セキュリティヘッダーミドルウェア
 */
function securityHeaders(req, res, next) {
  // セキュリティ関連のHTTPヘッダーを設定
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  
  // 開発環境では緩い設定、本番環境では厳格に
  if (process.env.NODE_ENV === 'production') {
    res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
    res.setHeader('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'");
  }
  
  next();
}

module.exports = {
  authenticateAPIKey,
  rateLimit,
  optionalAuth,
  securityHeaders,
  AUTH_CONFIG
};