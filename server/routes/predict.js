const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs').promises;
const fsSync = require('fs');
const UPLOAD_DIR = path.join(__dirname, '..', 'uploads');
const { spawn } = require('child_process');
const router = express.Router();
const storage = multer.diskStorage({
  destination: async (req, file, cb) => {
    const uploadDir = path.join(__dirname, '..', 'uploads');
    try {
      await fs.mkdir(uploadDir, { recursive: true });
      cb(null, uploadDir);
    } catch (error) {
      cb(error);
    }
  },
  filename: (req, file, cb) => {
    const timestamp = Date.now();
    const nanosecond = process.hrtime.bigint();
    const random = Math.round(Math.random() * 1E9);
    const uniqueSuffix = `${timestamp}-${nanosecond}-${random}`;
    const ext = path.extname(file.originalname);
    cb(null, `upload-${uniqueSuffix}${ext}`);
  }
});

const upload = multer({
  storage: storage,
  limits: {
    fileSize: 2 * 1024 * 1024
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('無効なファイルタイプです。JPEGおよびPNG画像のみ許可されています。'));
    }
  }
});

function callPythonScript(imagePath) {
  return new Promise((resolve, reject) => {
    const pythonScriptPath = path.join(__dirname, '..', '..', 'ml', 'predict.py');
    let pythonPath = process.env.PYTHON_PATH || 'python3';
    
    if (!path.isAbsolute(pythonPath)) {
      pythonPath = path.join(__dirname, '..', '..', pythonPath);
    }
    
    if (process.platform === 'win32') {
      const venvPythonWin = path.join(__dirname, '..', '..', 'venv', 'Scripts', 'python.exe');
      pythonPath = venvPythonWin;
    }
    
    console.log(`Python実行パス: ${pythonPath}`);
    console.log(`Pythonスクリプトパス: ${pythonScriptPath}`);
    
    const pythonProcess = spawn(pythonPath, [pythonScriptPath, imagePath]);
    let stdout = '';
    let stderr = '';
    
    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });
    
    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    
    pythonProcess.on('close', (code) => {
      if (code === 0) {
        try {
          const result = JSON.parse(stdout.trim());
          resolve(result);
        } catch (error) {
          reject(new Error(`Python出力のパースに失敗しました: ${stdout}`));
        }
      } else {
        reject(new Error(`Pythonスクリプトがコード${code}で失敗しました: ${stderr}`));
      }
    });
    
    pythonProcess.on('error', (error) => {
      reject(new Error(`Pythonスクリプトの起動に失敗しました: ${error.message}`));
    });
  });
}

function cleanupFileSync(filePath) {
  try {
    // Ensure the file is within the upload directory
    const resolvedPath = path.resolve(filePath);
    const resolvedUploadDir = path.resolve(UPLOAD_DIR);
    const relativePath = path.relative(resolvedUploadDir, resolvedPath);
    
    // Check if the path is outside the upload directory (starts with '..' or is absolute)
    if (relativePath.startsWith('..') || path.isAbsolute(relativePath)) {
      console.warn(`警告: アップロードディレクトリ外のファイル削除要求: ${resolvedPath}`);
      return false;
    }
    
    // Check if file exists before attempting to delete
    if (fsSync.existsSync(resolvedPath)) {
      fsSync.unlinkSync(resolvedPath);
      console.log(`ファイル削除完了: ${path.basename(resolvedPath)}`);
      return true;
    } else {
      console.warn(`ファイルが存在しません: ${resolvedPath}`);
      return false;
    }
  } catch (error) {
    console.error('ファイルの清掃エラー:', error.message);
    return false;
  }
}

router.post('/predict', upload.single('image'), async (req, res) => {
  let uploadedFilePath = null;
  
  try {
    if (!req.file) {
      return res.status(400).json({
        error: '画像ファイルが提供されていません',
        message: '画像ファイルをアップロードしてください'
      });
    }
    
    uploadedFilePath = req.file.path;
    
    console.log(`画像を処理中: ${req.file.originalname}`);
    console.log(`ファイルサイズ: ${req.file.size} バイト`);
    console.log(`一意ファイル名: ${path.basename(uploadedFilePath)}`);
    
    const result = await callPythonScript(uploadedFilePath);
    
    if (result.error) {
      throw new Error(result.error);
    }
    
    console.log(`予測結果: ${result.digit} (信頼度: ${result.confidence})`);
    
    // Clean up the file before sending response to ensure it's deleted
    const cleanupSuccess = cleanupFileSync(uploadedFilePath);
    uploadedFilePath = null; // Prevent cleanup in finally block
    
    res.json({
      success: true,
      prediction: result.digit,
      confidence: result.confidence,
      filename: req.file.originalname,
      fileKey: req.body.fileKey
    });
    
  } catch (error) {
    console.error('予測エラー:', error.message);
    
    res.status(500).json({
      error: '予測に失敗しました',
      message: error.message
    });
    
  } finally {
    // Only cleanup if not already cleaned up in the try block
    if (uploadedFilePath) {
      cleanupFileSync(uploadedFilePath);
    }
  }
});

module.exports = router;