# API仕様

## エンドポイント一覧

### POST /api/predict

数字認識用の画像をアップロードします。

#### リクエスト

- **メソッド**: `POST`
- **コンテンツタイプ**: `multipart/form-data`
- **ボディ**: `image`フィールドを含むフォームデータ

#### レスポンス

##### 成功時

```json
{
  "success": true,
  "prediction": 7,
  "confidence": 0.95,
  "filename": "example.png"
}
```

- `success`: 処理成功フラグ
- `prediction`: 予測された数字 (0-9)
- `confidence`: 信頼度スコア (0-1)
- `filename`: アップロードされたファイル名

##### エラー時

```json
{
  "error": "予測に失敗しました",
  "message": "エラーの詳細"
}
```

#### 制限事項

- ファイル形式: JPEG, PNG のみ
- ファイルサイズ: 最大2MB
- サポート画像: 手書き数字のみ

### GET /api/health

ヘルスチェックエンドポイントです。

#### リクエスト

- **メソッド**: `GET`
- **パラメータ**: なし

#### レスポンス

```json
{
  "status": "サーバーが実行中です",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

## エラーコード

| HTTPステータス | エラーメッセージ | 説明 |
|---------------|-----------------|-----|
| 400 | ファイルがアップロードされていません | 画像ファイルが含まれていない |
| 400 | サポートされていないファイル形式です | JPEG/PNG以外のファイル |
| 413 | ファイルサイズが大きすぎます | 2MBを超えるファイル |
| 500 | 予測に失敗しました | Python処理エラー |

## 使用例

### JavaScript (fetch)

```javascript
const formData = new FormData();
formData.append('image', file);

fetch('/api/predict', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('予測結果:', data.prediction);
  console.log('信頼度:', data.confidence);
});
```

### curl

```bash
curl -X POST \
  -F "image=@/path/to/digit.png" \
  http://localhost:5000/api/predict
```

## レート制限

現在レート制限は設定されていませんが、本番環境では適切な制限を設けることを推奨します。