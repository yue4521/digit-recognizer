// 必要なモジュールをインポート
const express = require('express');        // Expressフレームワーク
const multer = require('multer');          // ファイルアップロード処理
const path = require('path');              // ファイルパス操作
const fs = require('fs').promises;         // ファイルシステム操作（Promise版）
const { spawn } = require('child_process'); // 子プロセス実行用
const crypto = require('crypto');          // 暗号化・ハッシュ用
const router = express.Router();           // Expressルーターを作成

// 認証ミドルウェアをインポート
const { authenticateAPIKey, rateLimit } = require('../middleware/auth');

// 画像ファイルのマジックナンバー（ファイル署名）
const IMAGE_SIGNATURES = {
  'image/jpeg': [
    [0xFF, 0xD8, 0xFF],           // JPEG
  ],
  'image/png': [
    [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A] // PNG
  ]
};

/**
 * ファイルの署名（マジックナンバー）を検証
 * 
 * セキュリティ対策：
 * - MIMEタイプスプーフィング攻撃を防止
 * - 実際のファイル内容と拡張子の一致を確認
 */
async function validateFileSignature(filePath, expectedMimeType) {
  try {
    // ファイルの最初の16バイトを読み取り
    const fileHandle = await fs.open(filePath, 'r');
    const buffer = Buffer.alloc(16);
    await fileHandle.read(buffer, 0, 16, 0);
    await fileHandle.close();
    
    const fileBytes = Array.from(buffer);
    const signatures = IMAGE_SIGNATURES[expectedMimeType];
    
    if (!signatures) {
      throw new Error(`未対応のMIMEタイプです: ${expectedMimeType}`);
    }
    
    // 署名のいずれかとマッチするかチェック
    const isValid = signatures.some(signature => {
      return signature.every((byte, index) => fileBytes[index] === byte);
    });
    
    if (!isValid) {
      throw new Error(`ファイル署名が無効です。期待されるタイプ: ${expectedMimeType}`);
    }
    
    return true;
    
  } catch (error) {
    throw new Error(`ファイル署名検証エラー: ${error.message}`);
  }
}

/**
 * ファイルサイズとディメンションを検証
 */
async function validateImageConstraints(filePath) {
  const stats = await fs.stat(filePath);
  
  // ファイルサイズ制限（5MB）
  const MAX_FILE_SIZE = 5 * 1024 * 1024;
  if (stats.size > MAX_FILE_SIZE) {
    throw new Error(`ファイルサイズが大きすぎます: ${stats.size} bytes (最大: ${MAX_FILE_SIZE} bytes)`);
  }
  
  // 最小ファイルサイズ（100 bytes - 有効な画像の最小サイズ）
  const MIN_FILE_SIZE = 100;
  if (stats.size < MIN_FILE_SIZE) {
    throw new Error(`ファイルサイズが小さすぎます: ${stats.size} bytes (最小: ${MIN_FILE_SIZE} bytes)`);
  }
  
  return true;
}

// ファイルアップロード用のmulter設定
const storage = multer.diskStorage({
  // アップロード先ディレクトリを設定
  destination: async (req, file, cb) => {
    const uploadDir = path.join(__dirname, '..', 'uploads');
    try {
      // アップロード用ディレクトリを作成（なければ）
      await fs.mkdir(uploadDir, { recursive: true });
      cb(null, uploadDir);
    } catch (error) {
      cb(error);
    }
  },
  // ファイル名を設定
  filename: (req, file, cb) => {
    // タイムスタンプとランダム数で一意のファイル名を生成
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    const ext = path.extname(file.originalname);
    cb(null, `upload-${uniqueSuffix}${ext}`);
  }
});

// multerアップロード設定
const upload = multer({
  storage: storage,
  limits: {
    fileSize: 2 * 1024 * 1024 // 2MB制限
  },
  fileFilter: (req, file, cb) => {
    // ファイルタイプのチェック
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);  // 許可されたファイルタイプ
    } else {
      cb(new Error('無効なファイルタイプです。JPEGおよびPNG画像のみ許可されています。'));
    }
  }
});

// 許可されたPython実行パスのホワイトリスト
const ALLOWED_PYTHON_PATHS = [
  'python3',
  'python',
  '/usr/bin/python3',
  '/usr/bin/python',
  '/usr/local/bin/python3',
  '/usr/local/bin/python',
  // 仮想環境のパス
  path.join(__dirname, '..', '..', 'venv', 'bin', 'python'),
  path.join(__dirname, '..', '..', 'venv', 'Scripts', 'python.exe')
];

/**
 * Python実行パスをセキュアに検証・取得します
 * 
 * セキュリティ対策：
 * - ホワイトリストによる実行パス制限
 * - パストラバーサル攻撃の防止
 * - コマンドインジェクション対策
 */
function getSecurePythonPath() {
  // 環境変数からPythonパスを取得
  let pythonPath = process.env.PYTHON_PATH || 'python3';
  
  // パス正規化（セキュリティ対策）
  pythonPath = path.normalize(pythonPath);
  
  // 相対パスの場合は絶対パスに変換
  if (!path.isAbsolute(pythonPath)) {
    pythonPath = path.resolve(__dirname, '..', '..', pythonPath);
  }
  
  // ホワイトリストチェック
  const isAllowed = ALLOWED_PYTHON_PATHS.some(allowedPath => {
    const normalizedAllowed = path.resolve(allowedPath);
    return path.resolve(pythonPath) === normalizedAllowed;
  });
  
  if (!isAllowed) {
    throw new Error(`セキュリティエラー: 許可されていないPython実行パスです: ${pythonPath}`);
  }
  
  return pythonPath;
}

/**
 * 入力パスをセキュアに検証します
 * 
 * セキュリティ対策：
 * - パストラバーサル攻撃の防止
 * - 不正なファイルパスの検出
 */
function validateImagePath(imagePath) {
  // パス正規化
  const normalizedPath = path.normalize(imagePath);
  
  // パストラバーサル攻撃チェック
  if (normalizedPath.includes('..') || normalizedPath.startsWith('/')) {
    throw new Error('セキュリティエラー: 不正なファイルパスが検出されました');
  }
  
  // 許可されたアップロードディレクトリ内かチェック
  const uploadDir = path.join(__dirname, '..', 'uploads');
  const resolvedImagePath = path.resolve(imagePath);
  const resolvedUploadDir = path.resolve(uploadDir);
  
  if (!resolvedImagePath.startsWith(resolvedUploadDir)) {
    throw new Error('セキュリティエラー: 許可されていないディレクトリへのアクセスです');
  }
  
  return resolvedImagePath;
}

// Python予測スクリプトを呼び出すヘルパー関数
function callPythonScript(imagePath) {
  return new Promise((resolve, reject) => {
    try {
      // セキュアなPython実行パス取得
      const pythonPath = getSecurePythonPath();
      
      // 画像パスの検証
      const validatedImagePath = validateImagePath(imagePath);
      
      // Pythonスクリプトのパスを設定
      const pythonScriptPath = path.join(__dirname, '..', '..', 'ml', 'predict.py');
      
      console.log(`Python実行パス: ${pythonPath}`);
      console.log(`Pythonスクリプトパス: ${pythonScriptPath}`);
      console.log(`検証済み画像パス: ${validatedImagePath}`);
      
      // Pythonプロセスを起動
      const pythonProcess = spawn(pythonPath, [pythonScriptPath, validatedImagePath]);
    
    let stdout = '';  // 標準出力
    let stderr = '';  // エラー出力
    
    // 標準出力のデータを取得
    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });
    
    // エラー出力のデータを取得
    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    
    // プロセス終了時の処理
    pythonProcess.on('close', (code) => {
      if (code === 0) {
        try {
          // JSONレスポンスをパース
          const result = JSON.parse(stdout.trim());
          resolve(result);
        } catch (error) {
          reject(new Error(`Python出力のパースに失敗しました: ${stdout}`));
        }
      } else {
        reject(new Error(`Pythonスクリプトがコード${code}で失敗しました: ${stderr}`));
      }
    });
    
    // プロセス起動エラーの処理
    pythonProcess.on('error', (error) => {
      reject(new Error(`Pythonスクリプトの起動に失敗しました: ${error.message}`));
    });
    
    } catch (securityError) {
      // セキュリティ検証エラーの処理
      reject(securityError);
    }
  });
}

// アップロードされたファイルを清掃するヘルパー関数
async function cleanupFile(filePath) {
  try {
    await fs.unlink(filePath);  // ファイルを削除
  } catch (error) {
    console.error('ファイルの清掃エラー:', error.message);
  }
}

// POST /api/predict エンドポイント（認証とレート制限付き）
router.post('/predict', authenticateAPIKey, rateLimit, upload.single('image'), async (req, res) => {
  let uploadedFilePath = null;
  
  try {
    // ファイルがアップロードされたかチェック
    if (!req.file) {
      return res.status(400).json({
        error: '画像ファイルが提供されていません',
        message: '画像ファイルをアップロードしてください'
      });
    }
    
    uploadedFilePath = req.file.path;
    
    console.log(`画像を処理中: ${req.file.originalname}`);
    console.log(`ファイルサイズ: ${req.file.size} バイト`);
    
    // セキュリティ検証を実行
    await validateImageConstraints(uploadedFilePath);
    await validateFileSignature(uploadedFilePath, req.file.mimetype);
    
    console.log('ファイル検証が完了しました');
    
    // Python予測スクリプトを呼び出し
    const result = await callPythonScript(uploadedFilePath);
    
    // 予測が成功したかチェック
    if (result.error) {
      throw new Error(result.error);
    }
    
    console.log(`予測結果: ${result.digit} (信頼度: ${result.confidence})`);
    
    // 成功した予測結果を返却
    res.json({
      success: true,
      prediction: result.digit,
      confidence: result.confidence,
      filename: req.file.originalname
    });
    
  } catch (error) {
    console.error('予測エラー:', error.message);
    
    // エラーレスポンスを返却
    res.status(500).json({
      error: '予測に失敗しました',
      message: error.message
    });
    
  } finally {
    // アップロードされたファイルを必ず清掃
    if (uploadedFilePath) {
      await cleanupFile(uploadedFilePath);
    }
  }
});

module.exports = router;