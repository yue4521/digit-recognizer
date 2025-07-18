// 必要なモジュールをインポート
const express = require('express');        // Expressフレームワーク
const multer = require('multer');          // ファイルアップロード処理
const path = require('path');              // ファイルパス操作
const fs = require('fs').promises;         // ファイルシステム操作（Promise版）
const { spawn } = require('child_process'); // 子プロセス実行用
const router = express.Router();           // Expressルーターを作成

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

// Python予測スクリプトを呼び出すヘルパー関数
function callPythonScript(imagePath) {
  return new Promise((resolve, reject) => {
    // Pythonスクリプトのパスを設定
    const pythonScriptPath = path.join(__dirname, '..', '..', 'ml', 'predict.py');
    const pythonCommand = process.platform === 'win32' ? 'python' : 'python3';
    
    // 仮想環境のPythonパスを設定
    const venvPython = path.join(__dirname, '..', '..', 'venv', 'bin', 'python3');
    const venvPythonWin = path.join(__dirname, '..', '..', 'venv', 'Scripts', 'python.exe');
    
    let pythonPath = pythonCommand;
    
    // 仮想環境のPythonを使用しようとする
    if (process.platform === 'win32') {
      pythonPath = venvPythonWin;  // Windows用
    } else {
      pythonPath = venvPython;     // macOS/Linux用
    }
    
    // Pythonプロセスを起動
    const pythonProcess = spawn(pythonPath, [pythonScriptPath, imagePath]);
    
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

// POST /api/predict エンドポイント
router.post('/predict', upload.single('image'), async (req, res) => {
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