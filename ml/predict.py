#!/usr/bin/env python3
"""
数字認識予測スクリプト。
アップロードされた画像を処理し、訓練済みSVMモデルを使用して数字を予測します。

新人エンジニア向け解説：
- このスクリプトはNode.jsサーバーから呼び出されます
- コマンドライン引数で画像ファイルパスを受け取ります
- 結果はJSON形式で標準出力に出力します
"""

# 必要なライブラリをインポート
import sys              # システム操作用（コマンドライン引数等）
import json             # JSONデータの処理用
import numpy as np      # 数値計算ライブラリ
from PIL import Image, ImageOps  # 画像処理ライブラリ
import joblib           # 機械学習モデルの読み込み用
import os               # ファイル操作用
from io import BytesIO  # バイナリデータの処理用

def detect_background_color(image):
    """
    画像の四隅から主な背景色（黒または白）を検出します。
    
    新人エンジニア向け解説：
    - 画像の四隅をサンプリングして背景色を推定します
    - MNISTデータは黒背景に白数字なので、色を合わせる必要があります
    
    戻り値: 'black' または 'white'
    """
    # グレースケールに変換（まだでない場合）
    if image.mode != 'L':
        image = image.convert('L')
    
    # 背景色を判定するために四隅のピクセルをサンプリング
    width, height = image.size
    corner_pixels = [
        image.getpixel((0, 0)),            # 左上
        image.getpixel((width-1, 0)),      # 右上
        image.getpixel((0, height-1)),     # 左下
        image.getpixel((width-1, height-1)) # 右下
    ]
    
    # 四隅のピクセル値の平均を計算
    avg_corner = np.mean(corner_pixels)
    
    # 平均値が127より大きい場合は白背景、そうでなければ黒背景
    return 'white' if avg_corner > 127 else 'black'

def preprocess_image(image_path):
    """
    数字認識のために画像を前処理します。
    
    新人エンジニア向け解説：
    この関数はMNISTデータセットと同じ形式にするための処理です：
    1. グレースケールに変換
    2. 正方形にパディングを追加
    3. 28x28ピクセルにリサイズ
    4. 0-1の範囲に正規化
    5. 必要に応じて色を反転（黒背景に白数字に統一）
    """
    try:
        # 画像ファイルを読み込み
        image = Image.open(image_path)
        
        # グレースケールに変換（カラー画像を白黒に）
        image = image.convert('L')
        
        # 背景色を検出
        bg_color = detect_background_color(image)
        
        # 背景が白の場合、黒背景にするために色を反転
        if bg_color == 'white':
            image = ImageOps.invert(image)
        
        # 画像のサイズを取得
        width, height = image.size
        
        # 黒でパディングして正方形にする（反転後の背景色）
        max_dim = max(width, height)
        
        # 黒背景の新しい正方形画像を作成
        square_image = Image.new('L', (max_dim, max_dim), color=0)
        
        # 元の画像を中央に貼り付け
        paste_x = (max_dim - width) // 2   # 水平方向の位置
        paste_y = (max_dim - height) // 2  # 垂直方向の位置
        square_image.paste(image, (paste_x, paste_y))
        
        # 28x28ピクセルにリサイズ（MNISTサイズ）
        resized_image = square_image.resize((28, 28), Image.Resampling.LANCZOS)
        
        # NumPy配列に変換
        image_array = np.array(resized_image)
        
        # 0-1の範囲に正規化（元々は0-255の範囲）
        image_array = image_array.astype(np.float32) / 255.0
        
        # 1次元配列に変換（784の特徴量）
        # 28x28 = 784ピクセルのフラットな配列になります
        image_flattened = image_array.flatten()
        
        return image_flattened
        
    except Exception as e:
        raise Exception(f"画像の前処理中にエラーが発生しました: {str(e)}")

def predict_digit(image_path):
    """
    前処理した画像から訓練済みSVMモデルを使用して数字を予測します。
    
    新人エンジニア向け解説：
    1. 保存されたモデルファイルを読み込み
    2. 画像を前処理してモデルが期待する形式に変換
    3. モデルで予測を実行
    4. 予測結果と信頼度を返却
    """
    try:
        # 訓練済みモデルを読み込み
        model_path = os.path.join(os.path.dirname(__file__), 'svm_model.pkl')
        
        # モデルファイルの存在を確認
        if not os.path.exists(model_path):
            raise Exception(f"モデルファイルが見つかりません: {model_path}")
        
        # joblibでモデルを読み込み
        clf = joblib.load(model_path)
        
        # 画像を前処理して特徴量を抽出
        image_features = preprocess_image(image_path)
        
        # 予測用に形状を変更（モデルは2次元配列を期待）
        # (784,) -> (1, 784) の形状に変更
        image_features = image_features.reshape(1, -1)
        
        # モデルで予測を実行
        prediction = clf.predict(image_features)[0]
        
        # 予測の信頼度を取得（決定関数の値）
        confidence_scores = clf.decision_function(image_features)[0]
        max_confidence = np.max(confidence_scores)
        
        # 結果を辞書形式で返却
        return {
            "digit": int(prediction),           # 予測された数字
            "confidence": float(max_confidence) # 信頼度スコア
        }
        
    except Exception as e:
        raise Exception(f"予測中にエラーが発生しました: {str(e)}")

def main():
    """
    コマンドライン引数を処理し、JSON結果を出力するメイン関数。
    
    新人エンジニア向け解説：
    - Node.jsサーバーから呼び出されることを前提としています
    - コマンドライン引数で画像ファイルパスを受け取ります
    - 結果はJSON形式で標準出力に出力します
    """
    # コマンドライン引数の数をチェック
    if len(sys.argv) != 2:
        print(json.dumps({"error": "使用方法: python predict.py <画像ファイルパス>"}))
        sys.exit(1)
    
    # コマンドライン引数から画像ファイルパスを取得
    image_path = sys.argv[1]
    
    try:
        # 画像ファイルが存在するか確認
        if not os.path.exists(image_path):
            raise Exception(f"画像ファイルが見つかりません: {image_path}")
        
        # 数字を予測
        result = predict_digit(image_path)
        
        # 結果をJSON形式で出力
        print(json.dumps(result))
        
    except Exception as e:
        # エラーをJSON形式で出力
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

# メイン処理：スクリプトが直接実行された場合のみ実行されます
if __name__ == "__main__":
    main()