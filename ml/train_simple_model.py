#!/usr/bin/env python3
"""
シンプルなMNIST風数字認識モデル訓練スクリプト
SSL証明書問題を回避するため、自作のMNISTライクなデータでモデルを訓練します。
"""

import numpy as np
from sklearn import svm
import joblib
import os
from PIL import Image, ImageDraw


def generate_digit_data():
    """
    各数字（0-9）のより多様なトレーニングデータを生成
    """
    print("数字データを生成中...")

    data = []
    labels = []

    # 各数字について複数のパターンを生成
    for digit in range(10):
        for variation in range(200):  # 各数字200パターンに増加
            # 28x28の黒画像を作成
            img = Image.new("L", (28, 28), color=0)
            draw = ImageDraw.Draw(img)

            # より大きなランダム性を追加
            x_offset = np.random.randint(-3, 4)
            y_offset = np.random.randint(-3, 4)
            line_width = np.random.randint(1, 3)

            # 各数字の特徴的な描画パターンを改善
            if digit == 0:
                # 楕円と長方形の組み合わせでバリエーション
                if variation % 3 == 0:
                    draw.ellipse(
                        [6 + x_offset, 4 + y_offset, 22 + x_offset, 24 + y_offset],
                        outline=255,
                        width=line_width,
                    )
                elif variation % 3 == 1:
                    draw.rectangle(
                        [8 + x_offset, 6 + y_offset, 20 + x_offset, 22 + y_offset],
                        outline=255,
                        width=line_width,
                    )
                else:
                    # 楕円の中に小さな楕円
                    draw.ellipse(
                        [6 + x_offset, 4 + y_offset, 22 + x_offset, 24 + y_offset],
                        outline=255,
                        width=line_width,
                    )
                    draw.ellipse(
                        [10 + x_offset, 8 + y_offset, 18 + x_offset, 20 + y_offset],
                        outline=0,
                        width=1,
                    )

            elif digit == 1:
                # 直線と角度のある線のバリエーション
                if variation % 2 == 0:
                    draw.line(
                        [14 + x_offset, 4 + y_offset, 14 + x_offset, 24 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                    draw.line(
                        [12 + x_offset, 6 + y_offset, 14 + x_offset, 4 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                else:
                    draw.line(
                        [13 + x_offset, 4 + y_offset, 13 + x_offset, 24 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                    draw.line(
                        [10 + x_offset, 24 + y_offset, 16 + x_offset, 24 + y_offset],
                        fill=255,
                        width=line_width,
                    )

            elif digit == 2:
                # S字カーブとジグザグパターン
                if variation % 2 == 0:
                    draw.arc(
                        [6 + x_offset, 4 + y_offset, 22 + x_offset, 12 + y_offset],
                        0,
                        180,
                        fill=255,
                        width=line_width,
                    )
                    draw.line(
                        [22 + x_offset, 12 + y_offset, 6 + x_offset, 24 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                    draw.line(
                        [6 + x_offset, 24 + y_offset, 22 + x_offset, 24 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                else:
                    draw.line(
                        [6 + x_offset, 4 + y_offset, 22 + x_offset, 4 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                    draw.line(
                        [22 + x_offset, 4 + y_offset, 6 + x_offset, 14 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                    draw.line(
                        [6 + x_offset, 14 + y_offset, 22 + x_offset, 24 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                    draw.line(
                        [6 + x_offset, 24 + y_offset, 22 + x_offset, 24 + y_offset],
                        fill=255,
                        width=line_width,
                    )

            elif digit == 3:
                # 複数の曲線パターン
                draw.line(
                    [6 + x_offset, 4 + y_offset, 20 + x_offset, 4 + y_offset],
                    fill=255,
                    width=line_width,
                )
                draw.arc(
                    [14 + x_offset, 4 + y_offset, 22 + x_offset, 12 + y_offset],
                    270,
                    90,
                    fill=255,
                    width=line_width,
                )
                draw.arc(
                    [14 + x_offset, 16 + y_offset, 22 + x_offset, 24 + y_offset],
                    270,
                    90,
                    fill=255,
                    width=line_width,
                )
                draw.line(
                    [6 + x_offset, 24 + y_offset, 20 + x_offset, 24 + y_offset],
                    fill=255,
                    width=line_width,
                )

            elif digit == 4:
                # L字型とT字型のバリエーション
                if variation % 2 == 0:
                    draw.line(
                        [6 + x_offset, 4 + y_offset, 6 + x_offset, 14 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                    draw.line(
                        [6 + x_offset, 14 + y_offset, 22 + x_offset, 14 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                    draw.line(
                        [20 + x_offset, 4 + y_offset, 20 + x_offset, 24 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                else:
                    draw.line(
                        [8 + x_offset, 4 + y_offset, 18 + x_offset, 14 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                    draw.line(
                        [6 + x_offset, 14 + y_offset, 22 + x_offset, 14 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                    draw.line(
                        [18 + x_offset, 4 + y_offset, 18 + x_offset, 24 + y_offset],
                        fill=255,
                        width=line_width,
                    )

            elif digit == 5:
                # S字型の変形パターン
                draw.line(
                    [6 + x_offset, 4 + y_offset, 20 + x_offset, 4 + y_offset],
                    fill=255,
                    width=line_width,
                )
                draw.line(
                    [6 + x_offset, 4 + y_offset, 6 + x_offset, 14 + y_offset],
                    fill=255,
                    width=line_width,
                )
                draw.line(
                    [6 + x_offset, 14 + y_offset, 18 + x_offset, 14 + y_offset],
                    fill=255,
                    width=line_width,
                )
                draw.arc(
                    [14 + x_offset, 14 + y_offset, 22 + x_offset, 24 + y_offset],
                    270,
                    180,
                    fill=255,
                    width=line_width,
                )
                draw.line(
                    [6 + x_offset, 24 + y_offset, 18 + x_offset, 24 + y_offset],
                    fill=255,
                    width=line_width,
                )

            elif digit == 6:
                # 円と半円の組み合わせ
                if variation % 2 == 0:
                    draw.arc(
                        [6 + x_offset, 4 + y_offset, 22 + x_offset, 24 + y_offset],
                        90,
                        270,
                        fill=255,
                        width=line_width,
                    )
                    draw.ellipse(
                        [8 + x_offset, 14 + y_offset, 20 + x_offset, 24 + y_offset],
                        outline=255,
                        width=line_width,
                    )
                else:
                    draw.line(
                        [14 + x_offset, 4 + y_offset, 6 + x_offset, 14 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                    draw.ellipse(
                        [6 + x_offset, 14 + y_offset, 22 + x_offset, 24 + y_offset],
                        outline=255,
                        width=line_width,
                    )

            elif digit == 7:
                # 直線と角度のバリエーション
                if variation % 3 == 0:
                    draw.line(
                        [6 + x_offset, 4 + y_offset, 22 + x_offset, 4 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                    draw.line(
                        [22 + x_offset, 4 + y_offset, 10 + x_offset, 24 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                elif variation % 3 == 1:
                    draw.line(
                        [6 + x_offset, 4 + y_offset, 20 + x_offset, 4 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                    draw.line(
                        [18 + x_offset, 4 + y_offset, 8 + x_offset, 24 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                    draw.line(
                        [10 + x_offset, 14 + y_offset, 16 + x_offset, 14 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                else:
                    draw.polygon(
                        [
                            (6 + x_offset, 4 + y_offset),
                            (22 + x_offset, 4 + y_offset),
                            (12 + x_offset, 24 + y_offset),
                        ],
                        outline=255,
                        width=line_width,
                    )

            elif digit == 8:
                # 8の字の特徴を弱くするため、異なるパターンを採用
                if variation % 3 == 0:
                    # 上下の円を少しずらす
                    draw.ellipse(
                        [6 + x_offset, 4 + y_offset, 18 + x_offset, 14 + y_offset],
                        outline=255,
                        width=line_width,
                    )
                    draw.ellipse(
                        [10 + x_offset, 14 + y_offset, 22 + x_offset, 24 + y_offset],
                        outline=255,
                        width=line_width,
                    )
                elif variation % 3 == 1:
                    # 長方形の組み合わせ
                    draw.rectangle(
                        [8 + x_offset, 4 + y_offset, 20 + x_offset, 14 + y_offset],
                        outline=255,
                        width=line_width,
                    )
                    draw.rectangle(
                        [8 + x_offset, 14 + y_offset, 20 + x_offset, 24 + y_offset],
                        outline=255,
                        width=line_width,
                    )
                else:
                    # 重なる円
                    draw.ellipse(
                        [6 + x_offset, 4 + y_offset, 22 + x_offset, 16 + y_offset],
                        outline=255,
                        width=line_width,
                    )
                    draw.ellipse(
                        [6 + x_offset, 12 + y_offset, 22 + x_offset, 24 + y_offset],
                        outline=255,
                        width=line_width,
                    )

            elif digit == 9:
                # 6の反転とP字型のバリエーション
                if variation % 2 == 0:
                    draw.ellipse(
                        [6 + x_offset, 4 + y_offset, 22 + x_offset, 14 + y_offset],
                        outline=255,
                        width=line_width,
                    )
                    draw.line(
                        [22 + x_offset, 14 + y_offset, 14 + x_offset, 24 + y_offset],
                        fill=255,
                        width=line_width,
                    )
                else:
                    draw.arc(
                        [6 + x_offset, 4 + y_offset, 22 + x_offset, 24 + y_offset],
                        270,
                        90,
                        fill=255,
                        width=line_width,
                    )
                    draw.ellipse(
                        [8 + x_offset, 4 + y_offset, 20 + x_offset, 14 + y_offset],
                        outline=255,
                        width=line_width,
                    )

            # より強いノイズとぼかし効果を追加
            img_array = np.array(img)

            # ガウシアンノイズを追加
            noise = np.random.normal(0, 15, img_array.shape)
            img_array = np.clip(img_array + noise, 0, 255)

            # ランダムに回転を追加
            if variation % 4 == 0:
                rotation_angle = np.random.randint(-15, 16)
                img = Image.fromarray(img_array.astype(np.uint8))
                img = img.rotate(rotation_angle, fillcolor=0)
                img_array = np.array(img)

            # データを正規化してリストに追加
            img_normalized = img_array.flatten() / 255.0
            data.append(img_normalized)
            labels.append(digit)

    return np.array(data), np.array(labels)


def train_svm_model():
    """
    改善されたSVMモデルを訓練し保存
    """
    # データを生成
    X, y = generate_digit_data()

    print(f"データセットサイズ: {len(X)} サンプル")
    print("SVMモデルを訓練中...")

    # データセットをシャッフル
    from sklearn.utils import shuffle

    X, y = shuffle(X, y, random_state=42)

    # 訓練・テストデータに分割
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 改善されたSVMモデルを作成（より適切なパラメータ）
    clf = svm.SVC(
        kernel="rbf",
        gamma="scale",
        C=10.0,  # より強い正則化
        random_state=42,
        class_weight="balanced",  # クラス不均衡を考慮
    )

    # モデルを訓練
    clf.fit(X_train, y_train)

    # 訓練とテストの精度を評価
    train_accuracy = clf.score(X_train, y_train)
    test_accuracy = clf.score(X_test, y_test)

    print(f"訓練精度: {train_accuracy:.4f}")
    print(f"テスト精度: {test_accuracy:.4f}")

    # 各クラスの予測結果を確認
    from sklearn.metrics import classification_report

    y_pred = clf.predict(X_test)
    print("\n分類レポート:")
    print(classification_report(y_test, y_pred))

    # モデルを保存
    model_path = os.path.join(os.path.dirname(__file__), "svm_model.pkl")
    joblib.dump(clf, model_path)
    print(f"モデルを保存しました: {model_path}")

    return clf, test_accuracy


if __name__ == "__main__":
    try:
        model, accuracy = train_svm_model()
        print(f"訓練が成功しました！ 精度: {accuracy:.4f}")
    except Exception as e:
        print(f"訓練中にエラーが発生しました: {e}")
        import sys

        sys.exit(1)
