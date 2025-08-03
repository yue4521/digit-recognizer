#!/usr/bin/env python3
"""
数字認識予測スクリプト。
アップロードされた画像を処理し、訓練済みSVMモデルを使用して数字を予測します。
"""

import sys
import json
import numpy as np
from PIL import Image, ImageOps
import joblib
import os


def detect_background_color(image):
    """
    画像の四隅から主な背景色（黒または白）を検出します。
    """
    if image.mode != "L":
        image = image.convert("L")

    width, height = image.size
    corner_pixels = [
        image.getpixel((0, 0)),
        image.getpixel((width - 1, 0)),
        image.getpixel((0, height - 1)),
        image.getpixel((width - 1, height - 1)),
    ]

    avg_corner = np.mean(corner_pixels)
    return "white" if avg_corner > 127 else "black"


def preprocess_image(image_path):
    """
    MNISTデータセットと同じ形式に画像を前処理します。
    """
    try:
        image = Image.open(image_path)
        image = image.convert("L")

        bg_color = detect_background_color(image)
        if bg_color == "white":
            image = ImageOps.invert(image)

        width, height = image.size
        max_dim = max(width, height)

        square_image = Image.new("L", (max_dim, max_dim), color=0)
        paste_x = (max_dim - width) // 2
        paste_y = (max_dim - height) // 2
        square_image.paste(image, (paste_x, paste_y))

        resized_image = square_image.resize((28, 28), Image.Resampling.LANCZOS)
        image_array = np.array(resized_image)
        image_array = image_array.astype(np.float32) / 255.0

        return image_array.flatten()

    except Exception as e:
        raise Exception(f"画像の前処理中にエラーが発生しました: {str(e)}")


def predict_digit(image_path):
    """
    訓練済みSVMモデルを使用して数字を予測します。
    """
    try:
        model_path = os.path.join(os.path.dirname(__file__), "svm_model.pkl")

        if not os.path.exists(model_path):
            raise Exception(f"モデルファイルが見つかりません: {model_path}")

        clf = joblib.load(model_path)
        image_features = preprocess_image(image_path)
        image_features = image_features.reshape(1, -1)

        prediction = clf.predict(image_features)[0]
        confidence_scores = clf.decision_function(image_features)[0]
        max_confidence = np.max(confidence_scores)
        normalized_confidence = 1.0 / (1.0 + np.exp(-max_confidence))

        return {"digit": int(prediction), "confidence": float(normalized_confidence)}

    except Exception as e:
        raise Exception(f"予測中にエラーが発生しました: {str(e)}")


def main():
    """
    コマンドライン引数から画像パスを受け取り、予測結果をJSON出力します。
    """
    if len(sys.argv) != 2:
        print(json.dumps({"error": "使用方法: python predict.py <画像ファイルパス>"}))
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        if not os.path.exists(image_path):
            raise Exception(f"画像ファイルが見つかりません: {image_path}")

        result = predict_digit(image_path)
        print(json.dumps(result))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
