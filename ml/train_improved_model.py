#!/usr/bin/env python3
"""
改善された数字認識モデル訓練スクリプト
より実際のテストデータに近い訓練データを生成
"""

import numpy as np
from sklearn import svm
import joblib
import os
from PIL import Image, ImageDraw, ImageFont

def create_font_based_digit(digit, size=(28, 28), variations=1):
    """
    フォントベースで数字画像を生成
    """
    images = []
    
    for _ in range(variations):
        # 28x28の黒画像を作成
        img = Image.new('L', size, color=0)
        draw = ImageDraw.Draw(img)
        
        # ランダム性を追加
        x_offset = np.random.randint(-2, 3)
        y_offset = np.random.randint(-2, 3)
        
        try:
            # デフォルトフォントを使用
            font = ImageFont.load_default()
            
            # テキストのサイズを取得して中央配置
            bbox = draw.textbbox((0, 0), str(digit), font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            text_x = (size[0] - text_width) // 2 + x_offset
            text_y = (size[1] - text_height) // 2 + y_offset
            
            draw.text((text_x, text_y), str(digit), fill=255, font=font)
            
        except Exception as e:
            print(f"フォント描画エラー（数字{digit}）: {e}")
            # フォールバック: 中央に大きなテキスト
            draw.text((10 + x_offset, 8 + y_offset), str(digit), fill=255)
        
        # 軽微なノイズを追加
        img_array = np.array(img)
        noise = np.random.normal(0, 5, img_array.shape)
        img_array = np.clip(img_array + noise, 0, 255)
        
        # 軽微な回転を追加
        if np.random.random() < 0.3:
            rotation_angle = np.random.randint(-10, 11)
            img_rotated = Image.fromarray(img_array.astype(np.uint8))
            img_rotated = img_rotated.rotate(rotation_angle, fillcolor=0)
            img_array = np.array(img_rotated)
        
        images.append(img_array)
    
    return images

def generate_balanced_dataset():
    """
    バランスの取れた訓練データセットを生成
    """
    print("改善されたデータセットを生成中...")
    
    data = []
    labels = []
    
    # 各数字について大量のバリエーションを生成
    for digit in range(10):
        print(f"数字 {digit} のデータを生成中...")
        
        # 各数字500サンプル生成
        digit_images = create_font_based_digit(digit, variations=500)
        
        for img_array in digit_images:
            # 正規化してリストに追加
            img_normalized = img_array.flatten() / 255.0
            data.append(img_normalized)
            labels.append(digit)
    
    return np.array(data), np.array(labels)

def train_improved_svm():
    """
    改善されたSVMモデルの訓練
    """
    # データセットを生成
    X, y = generate_balanced_dataset()
    
    print(f"データセットサイズ: {len(X)} サンプル")
    print("各数字のサンプル数:")
    for i in range(10):
        count = np.sum(y == i)
        print(f"  数字 {i}: {count} サンプル")
    
    # データをシャッフル
    from sklearn.utils import shuffle
    X, y = shuffle(X, y, random_state=42)
    
    # 訓練・テストデータに分割
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("SVMモデルを訓練中...")
    
    # SVMモデル
    clf = svm.SVC(
        kernel='rbf',
        gamma='scale',
        C=1.0,
        random_state=42,
        class_weight='balanced'
    )
    
    # 訓練
    clf.fit(X_train, y_train)
    
    # 評価
    train_accuracy = clf.score(X_train, y_train)
    test_accuracy = clf.score(X_test, y_test)
    
    print(f"訓練精度: {train_accuracy:.4f}")
    print(f"テスト精度: {test_accuracy:.4f}")
    
    # 詳細な分類レポート
    from sklearn.metrics import classification_report, confusion_matrix
    y_pred = clf.predict(X_test)
    
    print("\n分類レポート:")
    print(classification_report(y_test, y_pred))
    
    print("\n混同行列:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    # モデルを保存
    model_path = os.path.join(os.path.dirname(__file__), 'svm_model.pkl')
    joblib.dump(clf, model_path)
    print(f"\nモデルを保存しました: {model_path}")
    
    return clf, test_accuracy

if __name__ == "__main__":
    try:
        model, accuracy = train_improved_svm()
        print(f"\n訓練が完了しました！テスト精度: {accuracy:.4f}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import sys
        sys.exit(1)