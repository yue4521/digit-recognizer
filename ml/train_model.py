#!/usr/bin/env python3
"""
MNISTデータセットで数字認識用のSVMモデルを訓練するスクリプト。
"""

from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split
import joblib
import sys
import os


def train_svm_model():
    """
    MNISTデータセットでSVMモデルを訓練し、保存します。
    """
    print("MNISTデータセットを読み込み中...")
    mnist = datasets.fetch_openml("mnist_784", version=1, parser="auto")
    X, y = mnist.data, mnist.target.astype(int)

    X_subset = X[:10000]
    y_subset = y[:10000]

    X_train, X_val, y_train, y_val = train_test_split(
        X_subset, y_subset, test_size=0.2, random_state=42
    )

    print(f"訓練データセットサイズ: {len(X_train)}")
    print(f"検証データセットサイズ: {len(X_val)}")

    X_train = X_train / 255.0
    X_val = X_val / 255.0

    print("SVMモデルを訓練中...")
    clf = svm.SVC(kernel="rbf", gamma="scale", C=10, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_val)
    accuracy = metrics.accuracy_score(y_val, y_pred)

    print(f"検証精度: {accuracy:.4f}")
    print("分類レポート:")
    print(metrics.classification_report(y_val, y_pred))

    model_path = os.path.join(os.path.dirname(__file__), "svm_model.pkl")
    joblib.dump(clf, model_path)
    print(f"モデルを保存しました: {model_path}")

    return clf, accuracy


if __name__ == "__main__":
    try:
        model, accuracy = train_svm_model()
        print(f"訓練が成功しました！ 最終精度: {accuracy:.4f}")
    except Exception as e:
        print(f"訓練中にエラーが発生しました: {e}")
        sys.exit(1)
