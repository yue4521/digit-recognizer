#!/usr/bin/env python3
"""
テスト用のダミーSVMモデルを作成します。
MNISTデータセットの代わりに、簡単なダミーデータでモデルを訓練します。
"""

import numpy as np
import joblib
import os
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

def create_dummy_data():
    """
    ダミーの訓練データを作成します。
    各数字の特徴を模倣した784次元のベクトルを生成します。
    """
    # 各数字につき100サンプルを生成
    samples_per_digit = 100
    features = 784  # 28x28
    
    X = []
    y = []
    
    for digit in range(10):
        for _ in range(samples_per_digit):
            # 各数字に特徴的なパターンを持つダミーデータを生成
            # 実際のMNISTデータではありませんが、テスト用には十分です
            data = np.random.random(features) * 0.1  # 基本的にはノイズ
            
            # 数字に応じて特定の位置に強いシグナルを追加
            if digit == 0:
                # 0の形状を模倣: 外側の円
                data[100:150] = 0.8
                data[200:250] = 0.8
                data[600:650] = 0.8
            elif digit == 1:
                # 1の形状を模倣: 中央の縦線
                data[350:450] = 0.9
            elif digit == 2:
                # 2の形状を模倣: 上下の横線
                data[50:100] = 0.8
                data[700:750] = 0.8
            elif digit == 3:
                # 3の形状を模倣: 右側の曲線
                data[80:120] = 0.8
                data[400:440] = 0.8
                data[680:720] = 0.8
            elif digit == 4:
                # 4の形状を模倣: 左の縦線と中央の横線
                data[200:300] = 0.8
                data[400:500] = 0.8
            elif digit == 5:
                # 5の形状を模倣: 上の横線と中央の横線
                data[50:100] = 0.8
                data[400:450] = 0.8
            elif digit == 6:
                # 6の形状を模倣: 左の縦線と下の横線
                data[200:300] = 0.8
                data[650:750] = 0.8
            elif digit == 7:
                # 7の形状を模倣: 上の横線と右の斜線
                data[50:100] = 0.8
                data[300:400] = 0.7
            elif digit == 8:
                # 8の形状を模倣: 上下の横線と左右の縦線
                data[50:100] = 0.8
                data[200:250] = 0.8
                data[550:600] = 0.8
                data[650:750] = 0.8
            elif digit == 9:
                # 9の形状を模倣: 上の円と右の縦線
                data[50:150] = 0.8
                data[550:650] = 0.8
            
            X.append(data)
            y.append(digit)
    
    return np.array(X), np.array(y)

def create_dummy_model():
    """
    ダミーデータでSVMモデルを訓練し、保存します。
    """
    print("ダミーデータを生成中...")
    X, y = create_dummy_data()
    
    # 訓練・テストデータに分割
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print("SVMモデルを訓練中...")
    # SVMモデルを作成（シンプルなパラメータ）
    clf = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
    
    # モデルを訓練
    clf.fit(X_train, y_train)
    
    # テストデータでの精度を確認
    accuracy = clf.score(X_test, y_test)
    print(f"テストデータでの精度: {accuracy:.2f}")
    
    # モデルを保存
    model_path = os.path.join('ml', 'svm_model.pkl')
    joblib.dump(clf, model_path)
    print(f"モデルを保存しました: {model_path}")
    
    return clf

if __name__ == "__main__":
    create_dummy_model()