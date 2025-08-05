const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '..', '.env') });

const predictRoute = require('./routes/predict');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use('/api', predictRoute);
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'サーバーが実行中です', 
    timestamp: new Date().toISOString() 
  });
});

app.use((error, req, res, next) => {
  console.error('エラー:', error.message);
  res.status(500).json({
    error: '内部サーバーエラー',
    message: error.message
  });
});

app.use((req, res) => {
  res.status(404).json({
    error: '見つかりません',
    message: '要求されたリソースが見つかりませんでした'
  });
});
const server = app.listen(PORT, () => {
  console.log(`サーバーがポート ${PORT} で実行中`);
  console.log(`ヘルスチェック: http://localhost:${PORT}/api/health`);
});

process.on('SIGTERM', () => {
  console.log('SIGTERM受信: サーバーを正常終了中...');
  server.close(() => {
    console.log('サーバーが正常終了しました');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('SIGINT受信: サーバーを正常終了中...');
  server.close(() => {
    console.log('サーバーが正常終了しました');
    process.exit(0);
  });
});