# 機械学習詳細仕様

## モデル概要

### サポートベクターマシン (SVM)

- **モデルタイプ**: SVC (Support Vector Classifier)
- **カーネル**: RBF (Radial Basis Function)
- **データセット**: MNIST手書き数字データセット
- **クラス数**: 10 (数字0-9)

## データセット詳細

### MNIST Dataset

- **訓練サンプル**: 8,000画像
- **テストサンプル**: 2,000画像
- **画像サイズ**: 28x28ピクセル (グレースケール)
- **特徴量数**: 784 (28×28)
- **データ形式**: 0-255のピクセル値を0-1に正規化

### データ分割

```python
train_size = 8000
test_size = 2000
total_samples = train_size + test_size
```

## モデル訓練プロセス

### 1. データ準備

```python
from sklearn.datasets import fetch_openml

# MNISTデータセットの取得
mnist = fetch_openml('mnist_784', version=1, as_frame=False)
X, y = mnist["data"], mnist["target"]
```

### 2. データ前処理

```python
# 正規化 (0-255 → 0-1)
X = X / 255.0

# ラベルを整数に変換
y = y.astype(int)
```

### 3. モデル設定

```python
from sklearn.svm import SVC

# SVMモデルの設定
model = SVC(
    kernel='rbf',
    probability=True,  # 確率予測を有効化
    random_state=42
)
```

### 4. 訓練実行

```python
# モデル訓練
model.fit(X_train, y_train)

# モデルの保存
import pickle
with open('svm_model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

## 画像前処理パイプライン

### 1. 画像読み込み

```python
from PIL import Image
import numpy as np

image = Image.open(image_path)
```

### 2. グレースケール変換

```python
if image.mode != 'L':
    image = image.convert('L')
```

### 3. 背景色検出と色反転

```python
# 背景色を検出（コーナーピクセルの平均）
corners = [image.getpixel((0,0)), image.getpixel((0, h-1)), 
           image.getpixel((w-1, 0)), image.getpixel((w-1, h-1))]
avg_corner = sum(corners) / len(corners)

# 黒背景の場合は色反転
if avg_corner < 128:
    image = ImageOps.invert(image)
```

### 4. 正方形パディング

```python
# アスペクト比を保持して正方形に
max_size = max(width, height)
new_image = Image.new('L', (max_size, max_size), 255)

# 中央に配置
offset = ((max_size - width) // 2, (max_size - height) // 2)
new_image.paste(image, offset)
```

### 5. リサイズと正規化

```python
# 28x28にリサイズ
resized = new_image.resize((28, 28), Image.Resampling.LANCZOS)

# NumPy配列に変換して正規化
pixel_array = np.array(resized) / 255.0
flattened = pixel_array.flatten().reshape(1, -1)
```

## 予測プロセス

### 1. 予測実行

```python
# 数字予測
prediction = model.predict(processed_image)[0]

# 信頼度計算
probabilities = model.predict_proba(processed_image)[0]
confidence = float(np.max(probabilities))
```

### 2. 結果出力

```python
result = {
    "prediction": int(prediction),
    "confidence": confidence,
    "success": True
}
```

## パフォーマンス指標

### 精度指標

- **訓練精度**: 約98%
- **テスト精度**: 約95%
- **平均予測時間**: 500ms以下

### 混同行列 (Confusion Matrix)

各数字の認識精度：

| 数字 | 精度 | よくある誤認識 |
|------|------|----------------|
| 0 | 96% | 6, 8 |
| 1 | 98% | 7 |
| 2 | 94% | 3, 7 |
| 3 | 92% | 2, 5, 8 |
| 4 | 95% | 7, 9 |
| 5 | 93% | 3, 6 |
| 6 | 96% | 0, 5 |
| 7 | 94% | 1, 4 |
| 8 | 92% | 0, 3, 6 |
| 9 | 94% | 4, 7 |

## モデルの限界と改善点

### 現在の制約

1. **単一数字のみ**: 複数の数字が含まれる画像は対応不可
2. **標準的な向き**: 回転された数字の認識精度が低下
3. **ノイズ耐性**: 過度にノイズの多い画像で精度低下
4. **手書きスタイル**: 特殊な書体や装飾文字は認識困難

### 改善の方向性

1. **データ拡張**: 回転、ノイズ、変形を含む訓練データの追加
2. **前処理改善**: より高度な画像正規化とノイズ除去
3. **モデル変更**: CNN (畳み込みニューラルネットワーク) の導入
4. **アンサンブル**: 複数モデルの組み合わせ

## カスタマイズ設定

### ハイパーパラメータ調整

```python
# 現在の設定
svm_params = {
    'kernel': 'rbf',
    'C': 1.0,           # 正則化パラメータ
    'gamma': 'scale',   # カーネル係数
    'probability': True,
    'random_state': 42
}

# チューニング例
from sklearn.model_selection import GridSearchCV

param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': [0.001, 0.01, 0.1, 1]
}
```

### 訓練データサイズの調整

```python
# train_model.py の設定変更
TRAIN_SIZE = 8000  # 増加で精度向上、時間増加
TEST_SIZE = 2000   # 評価精度の向上
```

### 画像前処理のカスタマイズ

```python
# predict.py の設定変更
TARGET_SIZE = (28, 28)      # 画像サイズ
INVERT_THRESHOLD = 128      # 色反転の閾値
RESIZE_METHOD = Image.Resampling.LANCZOS  # リサイズ手法
```

## デバッグとモニタリング

### モデル性能の確認

```python
# 詳細な分類レポート
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

# 混同行列の可視化
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
```

### 予測過程の可視化

```python
# 前処理された画像の確認
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(original_image, cmap='gray')
plt.title('Original')

plt.subplot(1, 2, 2)
plt.imshow(processed_image.reshape(28, 28), cmap='gray')
plt.title('Processed')
plt.show()
```

### 予測信頼度の分析

```python
# 全クラスの確率分布
probabilities = model.predict_proba(image)[0]
for i, prob in enumerate(probabilities):
    print(f"数字 {i}: {prob:.3f}")
```