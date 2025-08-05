import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [fileKey, setFileKey] = useState(0);
  const [isPredicting, setIsPredicting] = useState(false);

  // コンポーネントのアンマウント時にURLをクリーンアップ
  useEffect(() => {
    return () => {
      if (previewUrl && previewUrl.startsWith('blob:')) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);
  const handleFileSelect = (file) => {
    if (!file) {
      setError('ファイルが選択されていません');
      return;
    }

    // MIMEタイプの基本チェック
    if (!(file.type === 'image/jpeg' || file.type === 'image/png')) {
      setError('有効な画像ファイル（JPEGまたはPNG）を選択してください');
      return;
    }

    // ファイルサイズ制限（10MB）
    const MAX_FILE_SIZE = 10 * 1024 * 1024;
    if (file.size > MAX_FILE_SIZE) {
      setError('ファイルサイズが大きすぎます（10MB以下にしてください）');
      return;
    }

    // FileReaderを使用した安全な画像読み込み
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        // 画像が正常に読み込まれた場合のみプレビューを設定
        setSelectedFile(file);
        setPreviewUrl(e.target.result);
        setPrediction(null);
        setError(null);
        setFileKey(prevKey => prevKey + 1);
        setIsPredicting(false);
      };
      img.onerror = () => {
        setError('無効な画像ファイルです');
      };
      img.src = e.target.result;
    };
    reader.onerror = () => {
      setError('ファイルの読み込みに失敗しました');
    };
    reader.readAsDataURL(file);
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    handleFileSelect(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handlePredict = async () => {
    if (!selectedFile) {
      setError('まず画像を選択してください');
      return;
    }

    if (isPredicting) {
      return;
    }

    setIsPredicting(true);
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const formData = new FormData();
      formData.append('image', selectedFile);
      formData.append('fileKey', fileKey.toString());

      const response = await fetch('/api/predict', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setPrediction({
          digit: data.prediction,
          confidence: data.confidence,
          filename: data.filename,
          fileKey: fileKey
        });
      } else {
        setError(data.message || '予測に失敗しました');
      }
    } catch (err) {
      setError('サーバーに接続できませんでした。再試行してください。');
    } finally {
      setLoading(false);
      setIsPredicting(false);
    }
  };

  const handleReset = () => {
    // メモリリークを防ぐため、前のURLをクリーンアップ
    if (previewUrl && previewUrl.startsWith('blob:')) {
      URL.revokeObjectURL(previewUrl);
    }
    setSelectedFile(null);
    setPreviewUrl(null);
    setPrediction(null);
    setError(null);
    setLoading(false);
    setIsPredicting(false);
    setFileKey(prevKey => prevKey + 1);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔢 手書き数字認識アプリ</h1>
        <p>手書き数字（0-9）の画像をアップロードして、AIによる予測を取得</p>
      </header>

      <main className="App-main">
        <div className="upload-section">
          <div 
            className={`upload-area ${dragOver ? 'drag-over' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            {previewUrl ? (
              <div className="preview-container">
                <img 
                  src={previewUrl} 
                  alt="Preview" 
                  className="preview-image"
                />
                <button 
                  className="reset-btn"
                  onClick={handleReset}
                >
                  ✕
                </button>
              </div>
            ) : (
              <div className="upload-placeholder">
                <div className="upload-icon">📷</div>
                <p>画像をここにドラッグ&ドロップするか、クリックして選択</p>
                <p className="upload-hint">JPEGおよびPNGファイルに対応</p>
              </div>
            )}
            
            <input
              type="file"
              accept="image/png,image/jpeg"
              onChange={handleFileChange}
              className="file-input"
            />
          </div>
        </div>

        <div className="action-section">
          <button
            className="predict-btn"
            onClick={handlePredict}
            disabled={!selectedFile || loading || isPredicting}
          >
            {loading ? '予測中...' : '数字を予測'}
          </button>
        </div>

        {loading && (
          <div className="loading-section">
            <div className="spinner"></div>
            <p>画像を分析中...</p>
          </div>
        )}

        {error && (
          <div className="error-section">
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          </div>
        )}

        {prediction && prediction.fileKey === fileKey && (
          <div className="result-section">
            <div className="result-container">
              <h2>予測結果</h2>
              <div className="predicted-digit">
                {prediction.digit}
              </div>
              <div className="confidence">
                信頼度: {(prediction.confidence * 100).toFixed(1)}%
              </div>
              <div className="filename">
                ファイル: {prediction.filename}
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>機械学習による駆動 • MNISTデータセットで訓練されたSVMモデル</p>
      </footer>
    </div>
  );
}

export default App;