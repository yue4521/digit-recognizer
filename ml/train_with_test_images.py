#!/usr/bin/env python3
"""
プロジェクトのテスト画像を使用してSVMモデルを訓練するスクリプト
"""

import numpy as np
from sklearn import svm
import joblib
import os
from PIL import Image, ImageOps
import glob


def preprocess_image(image_path):
    """
    predict.pyと同じ前処理を行う
    """
    try:
        # 画像ファイルを読み込み
        image = Image.open(image_path)

        # グレースケールに変換
        image = image.convert("L")

        # 背景色を検出
        width, height = image.size
        corner_pixels = [
            image.getpixel((0, 0)),
            image.getpixel((width - 1, 0)),
            image.getpixel((0, height - 1)),
            image.getpixel((width - 1, height - 1)),
        ]
        avg_corner = np.mean(corner_pixels)

        # 背景が白の場合、黒背景にするために色を反転
        if avg_corner > 127:
            image = ImageOps.invert(image)

        # 正方形にパディング
        width, height = image.size
        max_dim = max(width, height)
        square_image = Image.new("L", (max_dim, max_dim), color=0)
        paste_x = (max_dim - width) // 2
        paste_y = (max_dim - height) // 2
        square_image.paste(image, (paste_x, paste_y))

        # 28x28にリサイズ
        resized_image = square_image.resize((28, 28), Image.Resampling.LANCZOS)

        # NumPy配列に変換して正規化
        image_array = np.array(resized_image)
        image_array = image_array.astype(np.float32) / 255.0

        return image_array.flatten()

    except Exception as e:
        raise Exception(f"画像の前処理中にエラーが発生しました: {str(e)}")


def load_test_images():
    """
    テスト画像を読み込んでトレーニングデータを作成
    """
    print("テスト画像を読み込み中...")

    data = []
    labels = []

    # test/images/digits/フォルダから画像を読み込み
    test_dir = os.path.join(os.path.dirname(__file__), "..", "test", "images", "digits")

    for digit in range(10):
        # 各数字のファイルパターンを探す
        patterns = [f"{digit}.png", f"{digit}_black.png"]

        for pattern in patterns:
            image_path = os.path.join(test_dir, pattern)
            if os.path.exists(image_path):
                try:
                    # 画像を前処理
                    features = preprocess_image(image_path)

                    # データを追加（複数のバリエーションを作成）
                    for variation in range(20):  # 各画像から20のバリエーション
                        # ノイズを追加してデータ拡張
                        noisy_features = features + np.random.normal(
                            0, 0.05, features.shape
                        )
                        noisy_features = np.clip(noisy_features, 0, 1)

                        data.append(noisy_features)
                        labels.append(digit)

                    print(f"数字 {digit} の画像を読み込みました: {pattern}")
                except Exception as e:
                    print(f"画像 {image_path} の読み込みエラー: {e}")

    if len(data) == 0:
        raise Exception("テスト画像が見つかりません")

    return np.array(data), np.array(labels)


def create_additional_data():
    """
    基本的な数字パターンを追加で生成
    """
    print("追加の訓練データを生成中...")

    data = []
    labels = []

    # 各数字について基本パターンを生成
    for digit in range(10):
        for _ in range(50):  # 各数字50パターン
            # 28x28の基本的な数字パターンを作成
            pattern = np.zeros((28, 28))

            if digit == 0:
                # 楕円形
                for i in range(28):
                    for j in range(28):
                        dist = ((i - 14) / 10) ** 2 + ((j - 14) / 8) ** 2
                        if 0.7 < dist < 1.0:
                            pattern[i, j] = 1.0
            elif digit == 1:
                # 縦線
                for i in range(5, 23):
                    pattern[i, 12:16] = 1.0
            elif digit == 2:
                # S字型
                pattern[6:10, 8:20] = 1.0
                pattern[10:14, 15:20] = 1.0
                pattern[14:18, 8:15] = 1.0
                pattern[18:22, 8:20] = 1.0
            elif digit == 3:
                # 2つの半円
                for i in range(28):
                    for j in range(28):
                        if j > 14:
                            dist1 = ((i - 10) / 6) ** 2 + ((j - 18) / 4) ** 2
                            dist2 = ((i - 18) / 6) ** 2 + ((j - 18) / 4) ** 2
                            if 0.7 < dist1 < 1.0 or 0.7 < dist2 < 1.0:
                                pattern[i, j] = 1.0
            elif digit == 4:
                # L字 + 縦線
                pattern[6:18, 8:12] = 1.0
                pattern[14:18, 8:20] = 1.0
                pattern[18:22, 16:20] = 1.0
            elif digit == 5:
                # S字型（逆）
                pattern[6:10, 8:20] = 1.0
                pattern[10:14, 8:12] = 1.0
                pattern[14:18, 8:20] = 1.0
                pattern[18:22, 16:20] = 1.0
            elif digit == 6:
                # 螺旋状
                for i in range(28):
                    for j in range(28):
                        dist = ((i - 14) / 8) ** 2 + ((j - 14) / 8) ** 2
                        if 0.6 < dist < 1.0 and i > 14:
                            pattern[i, j] = 1.0
                        elif 0.3 < dist < 0.6 and i > 10:
                            pattern[i, j] = 1.0
            elif digit == 7:
                # 上線 + 斜線
                pattern[6:10, 8:20] = 1.0
                for i in range(10, 22):
                    j = 20 - (i - 10)
                    if 8 <= j <= 20:
                        pattern[i, j - 2 : j + 2] = 1.0
            elif digit == 8:
                # 2つの楕円
                for i in range(28):
                    for j in range(28):
                        dist1 = ((i - 10) / 5) ** 2 + ((j - 14) / 6) ** 2
                        dist2 = ((i - 18) / 5) ** 2 + ((j - 14) / 6) ** 2
                        if 0.7 < dist1 < 1.0 or 0.7 < dist2 < 1.0:
                            pattern[i, j] = 1.0
            elif digit == 9:
                # 逆6
                for i in range(28):
                    for j in range(28):
                        dist = ((i - 14) / 8) ** 2 + ((j - 14) / 8) ** 2
                        if 0.6 < dist < 1.0 and i < 14:
                            pattern[i, j] = 1.0
                        elif 0.3 < dist < 0.6 and i < 18:
                            pattern[i, j] = 1.0

            # ノイズを追加
            noise = np.random.normal(0, 0.1, pattern.shape)
            pattern = np.clip(pattern + noise, 0, 1)

            data.append(pattern.flatten())
            labels.append(digit)

    return np.array(data), np.array(labels)


def train_model():
    """
    モデルを訓練
    """
    try:
        # テスト画像からデータを読み込み
        test_data, test_labels = load_test_images()
        print(f"テスト画像データ: {len(test_data)} サンプル")

        # 追加データを生成
        additional_data, additional_labels = create_additional_data()
        print(f"追加データ: {len(additional_data)} サンプル")

        # データを結合
        X = np.vstack([test_data, additional_data])
        y = np.concatenate([test_labels, additional_labels])

        print(f"総データセットサイズ: {len(X)} サンプル")
        print(f"各クラスの分布: {np.bincount(y)}")

        # SVMモデルを作成
        print("SVMモデルを訓練中...")
        clf = svm.SVC(kernel="rbf", gamma="scale", C=1.0, random_state=42)
        clf.fit(X, y)

        # 訓練精度を計算
        train_accuracy = clf.score(X, y)
        print(f"訓練精度: {train_accuracy:.4f}")

        # モデルを保存
        model_path = os.path.join(os.path.dirname(__file__), "svm_model.pkl")
        joblib.dump(clf, model_path)
        print(f"モデルを保存しました: {model_path}")

        return clf, train_accuracy

    except Exception as e:
        raise Exception(f"モデル訓練中にエラーが発生しました: {str(e)}")


if __name__ == "__main__":
    try:
        model, accuracy = train_model()
        print(f"訓練が成功しました！ 精度: {accuracy:.4f}")
    except Exception as e:
        print(f"エラー: {e}")
        import sys

        sys.exit(1)
