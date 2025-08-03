#!/usr/bin/env python3
"""
シンプルなMNIST風数字認識モデル訓練スクリプト
SSL証明書問題を回避するため、自作のMNISTライクなデータでモデルを訓練します。
"""

import numpy as np
from sklearn import svm
import joblib
import os
from PIL import Image, ImageDraw, ImageFont


def generate_digit_data():
    """
    各数字（0-9）のシンプルなトレーニングデータを生成
    """
    print("数字データを生成中...")

    # 各数字のパターンを定義（28x28の簡易版）
    data = []
    labels = []

    # 各数字について複数のパターンを生成
    for digit in range(10):
        for variation in range(100):  # 各数字100パターン
            # 28x28の黒画像を作成
            img = Image.new("L", (28, 28), color=0)
            draw = ImageDraw.Draw(img)

            # 数字の位置とサイズにランダム性を追加
            x_offset = np.random.randint(-2, 3)
            y_offset = np.random.randint(-2, 3)
            font_size = np.random.randint(16, 22)

            try:
                # システムのデフォルトフォントを使用して数字を描画
                draw.text((10 + x_offset, 8 + y_offset), str(digit), fill=255)
            except:
                # フォントが利用できない場合は基本的な形で描画
                if digit == 0:
                    draw.ellipse(
                        [8 + x_offset, 6 + y_offset, 20 + x_offset, 22 + y_offset],
                        outline=255,
                        width=2,
                    )
                elif digit == 1:
                    draw.line(
                        [14 + x_offset, 6 + y_offset, 14 + x_offset, 22 + y_offset],
                        fill=255,
                        width=2,
                    )
                elif digit == 2:
                    draw.arc(
                        [8 + x_offset, 6 + y_offset, 20 + x_offset, 14 + y_offset],
                        0,
                        180,
                        fill=255,
                        width=2,
                    )
                    draw.line(
                        [20 + x_offset, 14 + y_offset, 8 + x_offset, 22 + y_offset],
                        fill=255,
                        width=2,
                    )
                    draw.line(
                        [8 + x_offset, 22 + y_offset, 20 + x_offset, 22 + y_offset],
                        fill=255,
                        width=2,
                    )
                elif digit == 3:
                    draw.arc(
                        [8 + x_offset, 6 + y_offset, 20 + x_offset, 14 + y_offset],
                        0,
                        180,
                        fill=255,
                        width=2,
                    )
                    draw.arc(
                        [8 + x_offset, 14 + y_offset, 20 + x_offset, 22 + y_offset],
                        0,
                        180,
                        fill=255,
                        width=2,
                    )
                elif digit == 4:
                    draw.line(
                        [8 + x_offset, 6 + y_offset, 8 + x_offset, 14 + y_offset],
                        fill=255,
                        width=2,
                    )
                    draw.line(
                        [8 + x_offset, 14 + y_offset, 20 + x_offset, 14 + y_offset],
                        fill=255,
                        width=2,
                    )
                    draw.line(
                        [20 + x_offset, 6 + y_offset, 20 + x_offset, 22 + y_offset],
                        fill=255,
                        width=2,
                    )
                elif digit == 5:
                    draw.line(
                        [8 + x_offset, 6 + y_offset, 20 + x_offset, 6 + y_offset],
                        fill=255,
                        width=2,
                    )
                    draw.line(
                        [8 + x_offset, 6 + y_offset, 8 + x_offset, 14 + y_offset],
                        fill=255,
                        width=2,
                    )
                    draw.line(
                        [8 + x_offset, 14 + y_offset, 20 + x_offset, 14 + y_offset],
                        fill=255,
                        width=2,
                    )
                    draw.line(
                        [20 + x_offset, 14 + y_offset, 20 + x_offset, 22 + y_offset],
                        fill=255,
                        width=2,
                    )
                    draw.line(
                        [8 + x_offset, 22 + y_offset, 20 + x_offset, 22 + y_offset],
                        fill=255,
                        width=2,
                    )
                elif digit == 6:
                    draw.ellipse(
                        [8 + x_offset, 6 + y_offset, 20 + x_offset, 22 + y_offset],
                        outline=255,
                        width=2,
                    )
                    draw.line(
                        [8 + x_offset, 14 + y_offset, 20 + x_offset, 14 + y_offset],
                        fill=255,
                        width=2,
                    )
                elif digit == 7:
                    draw.line(
                        [8 + x_offset, 6 + y_offset, 20 + x_offset, 6 + y_offset],
                        fill=255,
                        width=2,
                    )
                    draw.line(
                        [20 + x_offset, 6 + y_offset, 12 + x_offset, 22 + y_offset],
                        fill=255,
                        width=2,
                    )
                elif digit == 8:
                    draw.ellipse(
                        [8 + x_offset, 6 + y_offset, 20 + x_offset, 14 + y_offset],
                        outline=255,
                        width=2,
                    )
                    draw.ellipse(
                        [8 + x_offset, 14 + y_offset, 20 + x_offset, 22 + y_offset],
                        outline=255,
                        width=2,
                    )
                elif digit == 9:
                    draw.ellipse(
                        [8 + x_offset, 6 + y_offset, 20 + x_offset, 22 + y_offset],
                        outline=255,
                        width=2,
                    )
                    draw.line(
                        [8 + x_offset, 14 + y_offset, 20 + x_offset, 14 + y_offset],
                        fill=255,
                        width=2,
                    )

            # ノイズを追加
            img_array = np.array(img)
            noise = np.random.normal(0, 10, img_array.shape)
            img_array = np.clip(img_array + noise, 0, 255)

            # データを正規化してリストに追加
            img_normalized = img_array.flatten() / 255.0
            data.append(img_normalized)
            labels.append(digit)

    return np.array(data), np.array(labels)


def train_svm_model():
    """
    シンプルなSVMモデルを訓練し保存
    """
    # データを生成
    X, y = generate_digit_data()

    print(f"データセットサイズ: {len(X)} サンプル")
    print("SVMモデルを訓練中...")

    # SVMモデルを作成
    clf = svm.SVC(kernel="rbf", gamma="scale", C=1.0, random_state=42)

    # モデルを訓練
    clf.fit(X, y)

    # 簡単な評価
    train_accuracy = clf.score(X, y)
    print(f"訓練精度: {train_accuracy:.4f}")

    # モデルを保存
    model_path = os.path.join(os.path.dirname(__file__), "svm_model.pkl")
    joblib.dump(clf, model_path)
    print(f"モデルを保存しました: {model_path}")

    return clf, train_accuracy


if __name__ == "__main__":
    try:
        model, accuracy = train_svm_model()
        print(f"訓練が成功しました！ 精度: {accuracy:.4f}")
    except Exception as e:
        print(f"訓練中にエラーが発生しました: {e}")
        import sys

        sys.exit(1)
