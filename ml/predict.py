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
import time


def detect_background_color(image):
    """
    画像の四隅と縁から主な背景色（黒または白）を検出します。
    """
    if image.mode != "L":
        image = image.convert("L")

    width, height = image.size

    # 四隅の画素を取得
    corner_pixels = [
        image.getpixel((0, 0)),
        image.getpixel((width - 1, 0)),
        image.getpixel((0, height - 1)),
        image.getpixel((width - 1, height - 1)),
    ]

    # 上下左右の縁の画素もサンプリング
    edge_pixels = []
    for i in range(0, width, max(1, width // 10)):
        edge_pixels.append(image.getpixel((i, 0)))  # 上縁
        edge_pixels.append(image.getpixel((i, height - 1)))  # 下縁

    for i in range(0, height, max(1, height // 10)):
        edge_pixels.append(image.getpixel((0, i)))  # 左縁
        edge_pixels.append(image.getpixel((width - 1, i)))  # 右縁

    all_pixels = corner_pixels + edge_pixels
    avg_value = np.mean(all_pixels)

    return "white" if avg_value > 127 else "black"


def preprocess_image(image_path):
    """
    MNISTデータセットと同じ形式に画像を前処理します。
    """
    try:
        # Debug: Log processing start
        print(f"DEBUG: 画像前処理開始: {os.path.basename(image_path)}", file=sys.stderr)

        image = Image.open(image_path)
        original_size = image.size
        image = image.convert("L")

        bg_color = detect_background_color(image)
        print(f"DEBUG: 背景色検出: {bg_color}", file=sys.stderr)

        if bg_color == "white":
            image = ImageOps.invert(image)
            print("DEBUG: 白背景のため画像を反転", file=sys.stderr)

        width, height = image.size
        max_dim = max(width, height)

        # 正方形の画像を作成（黒背景）
        square_image = Image.new("L", (max_dim, max_dim), color=0)
        paste_x = (max_dim - width) // 2
        paste_y = (max_dim - height) // 2
        square_image.paste(image, (paste_x, paste_y))

        # 28x28にリサイズ
        resized_image = square_image.resize((28, 28), Image.Resampling.LANCZOS)
        image_array = np.array(resized_image)

        # 正規化
        image_array = image_array.astype(np.float32) / 255.0

        print(
            f"DEBUG: 前処理完了 - 元サイズ: {original_size}, 最終サイズ: {image_array.shape}",
            file=sys.stderr,
        )

        return image_array.flatten()

    except Exception as e:
        print(f"DEBUG: 前処理エラー: {str(e)}", file=sys.stderr)
        raise Exception(f"画像の前処理中にエラーが発生しました: {str(e)}")


def predict_digit(image_path):
    """
    訓練済みSVMモデルを使用して数字を予測します。
    """
    try:
        start_time = time.time()
        print(f"DEBUG: 予測開始: {os.path.basename(image_path)}", file=sys.stderr)

        model_path = os.path.join(os.path.dirname(__file__), "svm_model.pkl")

        if not os.path.exists(model_path):
            print(
                f"DEBUG: モデルファイルが見つかりません: {model_path}", file=sys.stderr
            )
            raise Exception(f"モデルファイルが見つかりません: {model_path}")

        print("DEBUG: モデル読み込み中...", file=sys.stderr)
        clf = joblib.load(model_path)

        print("DEBUG: 画像前処理中...", file=sys.stderr)
        image_features = preprocess_image(image_path)
        image_features = image_features.reshape(1, -1)

        print("DEBUG: 予測実行中...", file=sys.stderr)
        prediction = clf.predict(image_features)[0]
        confidence_scores = clf.decision_function(image_features)[0]
        max_confidence = np.max(confidence_scores)
        normalized_confidence = 1.0 / (1.0 + np.exp(-max_confidence))

        end_time = time.time()
        processing_time = end_time - start_time

        print(
            f"DEBUG: 予測完了 - 結果: {prediction}, 信頼度: {normalized_confidence:.3f}, 処理時間: {processing_time:.3f}秒",
            file=sys.stderr,
        )

        return {"digit": int(prediction), "confidence": float(normalized_confidence)}

    except Exception as e:
        print(f"DEBUG: 予測エラー: {str(e)}", file=sys.stderr)
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
        print(f"DEBUG: メイン関数開始 - 引数: {image_path}", file=sys.stderr)

        if not os.path.exists(image_path):
            print(f"DEBUG: ファイルが見つかりません: {image_path}", file=sys.stderr)
            raise Exception(f"画像ファイルが見つかりません: {image_path}")

        file_size = os.path.getsize(image_path)
        print(f"DEBUG: ファイル確認 - サイズ: {file_size} bytes", file=sys.stderr)

        result = predict_digit(image_path)
        print(f"DEBUG: 最終結果: {result}", file=sys.stderr)
        print(json.dumps(result))

    except Exception as e:
        print(f"DEBUG: メイン関数エラー: {str(e)}", file=sys.stderr)
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
