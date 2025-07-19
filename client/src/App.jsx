import React, { useState } from 'react';
import './App.css';

// メインのReactコンポーネント - 手書き数字認識アプリ
function App() {
  // 状態管理用のReact Hooks
  const [selectedFile, setSelectedFile] = useState(null);       // 選択されたファイル
  const [previewUrl, setPreviewUrl] = useState(null);           // プレビュー画像のURL
  const [prediction, setPrediction] = useState(null);           // 予測結果
  const [loading, setLoading] = useState(false);                // ローディング状態
  const [error, setError] = useState(null);                     // エラー状態
  const [dragOver, setDragOver] = useState(false);              // ドラッグオーバー状態

  // ファイル選択時の処理
  const handleFileSelect = (file) => {
    if (file && (file.type === 'image/jpeg' || file.type === 'image/png')) {
      setSelectedFile(file);                    // ファイルを状態に保存
      setPreviewUrl(URL.createObjectURL(file)); // プレビュー用URLを作成
      setPrediction(null);                      // 前回の予測結果をリセット
      setError(null);                           // エラーをリセット
    } else {
      setError('有効な画像ファイル（JPEGまたはPNG）を選択してください');
    }
  };

  // ファイル入力の変更時の処理
  const handleFileChange = (e) => {
    const file = e.target.files[0];  // 最初のファイルを取得
    handleFileSelect(file);           // ファイル選択処理を実行
  };

  // ドラッグオーバー時の処理
  const handleDragOver = (e) => {
    e.preventDefault();      // デフォルトの動作を無効化
    setDragOver(true);       // ドラッグオーバー状態を有効化
  };

  // ドラッグリーブ時の処理
  const handleDragLeave = (e) => {
    e.preventDefault();      // デフォルトの動作を無効化
    setDragOver(false);      // ドラッグオーバー状態を無効化
  };

  // ドロップ時の処理
  const handleDrop = (e) => {
    e.preventDefault();      // デフォルトの動作を無効化
    setDragOver(false);      // ドラッグオーバー状態を無効化
    
    const files = e.dataTransfer.files;  // ドロップされたファイルを取得
    if (files.length > 0) {
      handleFileSelect(files[0]);         // 最初のファイルを選択
    }
  };

  // 予測処理の実行
  const handlePredict = async () => {
    if (!selectedFile) {
      setError('まず画像を選択してください');
      return;
    }

    setLoading(true);         // ローディング状態を開始
    setError(null);           // エラーをリセット
    setPrediction(null);      // 前回の予測結果をリセット

    try {
      // FormDataオブジェクトを作成してファイルを追加
      const formData = new FormData();
      formData.append('image', selectedFile);

      // サーバーの予測APIにリクエストを送信
      // 開発環境では認証がバイパスされている場合があるため、APIキーは条件付きで送信
      const headers = {};
      
      // 本番環境または認証が有効な場合にAPIキーを送信
      if (process.env.NODE_ENV === 'production') {
        headers['x-api-key'] = process.env.REACT_APP_API_KEY || 'dev-api-key-12345';
      }
      
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: headers,
        body: formData,
      });

      const data = await response.json();

      // レスポンスが成功した場合
      if (response.ok && data.success) {
        setPrediction({
          digit: data.prediction,        // 予測された数字
          confidence: data.confidence,   // 信頼度
          filename: data.filename        // ファイル名
        });
      } else {
        setError(data.message || '予測に失敗しました');
      }
    } catch (err) {
      setError('サーバーに接続できませんでした。再試行してください。');
    } finally {
      setLoading(false);        // ローディング状態を終了
    }
  };

  // リセット処理
  const handleReset = () => {
    setSelectedFile(null);    // 選択されたファイルをクリア
    setPreviewUrl(null);      // プレビューURLをクリア
    setPrediction(null);      // 予測結果をクリア
    setError(null);           // エラーをクリア
    setLoading(false);        // ローディング状態をクリア
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
            disabled={!selectedFile || loading}
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

        {prediction && (
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