#!/usr/bin/env python3
"""
単体テスト用のサンプル画像生成スクリプト
手書き風の数字画像を生成します。
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random

def create_digit_image(digit, size=(64, 64), background_color='white'):
    """
    指定された数字の手書き風画像を生成します。
    
    Args:
        digit (int): 生成する数字 (0-9)
        size (tuple): 画像サイズ (width, height)
        background_color (str): 背景色 ('white' または 'black')
    
    Returns:
        PIL.Image: 生成された画像
    """
    # 背景色と文字色を設定
    if background_color == 'white':
        bg_color = (255, 255, 255)  # 白背景
        text_color = (0, 0, 0)      # 黒文字
    else:
        bg_color = (0, 0, 0)        # 黒背景
        text_color = (255, 255, 255)  # 白文字
    
    # 画像とドローオブジェクトを作成
    image = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(image)
    
    # フォントサイズを計算（画像サイズに基づく）
    font_size = min(size) * 3 // 4
    
    # システムフォントを使用（手書き風でないが、テスト用としては十分）
    try:
        # macOSの場合
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
    except:
        try:
            # Linuxの場合
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", font_size)
        except:
            # デフォルトフォントを使用
            font = ImageFont.load_default()
    
    # 数字をテキストとして描画
    digit_str = str(digit)
    
    # テキストの境界ボックスを取得
    bbox = draw.textbbox((0, 0), digit_str, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # テキストを中央に配置
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # 少しランダムなオフセットを追加して手書き風に
    x += random.randint(-3, 3)
    y += random.randint(-3, 3)
    
    draw.text((x, y), digit_str, fill=text_color, font=font)
    
    # 少しノイズを追加（手書き風の効果）
    pixels = np.array(image)
    for _ in range(random.randint(5, 15)):
        x_noise = random.randint(0, size[0] - 1)
        y_noise = random.randint(0, size[1] - 1)
        if background_color == 'white':
            pixels[y_noise, x_noise] = [200, 200, 200]  # 薄いグレー
        else:
            pixels[y_noise, x_noise] = [50, 50, 50]     # 濃いグレー
    
    return Image.fromarray(pixels)

def create_edge_case_image(image_type, digit=5, size=(64, 64)):
    """
    エッジケース画像を生成します。
    
    Args:
        image_type (str): 画像タイプ ('blurry', 'rotated', 'noisy')
        digit (int): 基準となる数字
        size (tuple): 画像サイズ
    
    Returns:
        PIL.Image: 生成された画像
    """
    # 基本画像を生成
    base_image = create_digit_image(digit, size)
    
    if image_type == 'blurry':
        # ぼやけた画像
        from PIL import ImageFilter
        return base_image.filter(ImageFilter.GaussianBlur(radius=2))
    
    elif image_type == 'rotated':
        # 回転した画像
        angle = random.randint(-30, 30)
        return base_image.rotate(angle, fillcolor=(255, 255, 255))
    
    elif image_type == 'noisy':
        # ノイズの多い画像
        pixels = np.array(base_image)
        noise = np.random.randint(0, 50, pixels.shape)
        noisy_pixels = np.clip(pixels + noise, 0, 255)
        return Image.fromarray(noisy_pixels.astype(np.uint8))
    
    return base_image

def create_invalid_image(image_type, size=(64, 64)):
    """
    無効な画像を生成します。
    
    Args:
        image_type (str): 画像タイプ ('not_digit', 'multiple_digits')
        size (tuple): 画像サイズ
    
    Returns:
        PIL.Image: 生成された画像
    """
    image = Image.new('RGB', size, (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    if image_type == 'not_digit':
        # 数字以外の文字（例：A）
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", size[0] * 3 // 4)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), "A", font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        draw.text((x, y), "A", fill=(0, 0, 0), font=font)
    
    elif image_type == 'multiple_digits':
        # 複数の数字
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", size[0] // 3)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), "12", font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        draw.text((x, y), "12", fill=(0, 0, 0), font=font)
    
    return image

def main():
    """メイン関数：テスト画像を生成します。"""
    base_dir = "test/images"
    
    # 基本数字画像を生成 (0-9)
    print("基本数字画像を生成中...")
    digits_dir = os.path.join(base_dir, "digits")
    for digit in range(10):
        # 白背景黒文字の画像
        image = create_digit_image(digit, size=(64, 64), background_color='white')
        image.save(os.path.join(digits_dir, f"{digit}.png"))
        
        # 黒背景白文字の画像も作成
        image_black = create_digit_image(digit, size=(64, 64), background_color='black')
        image_black.save(os.path.join(digits_dir, f"{digit}_black.png"))
    
    # エッジケース画像を生成
    print("エッジケース画像を生成中...")
    edge_cases_dir = os.path.join(base_dir, "edge_cases")
    
    # ぼやけた画像
    blurry_image = create_edge_case_image('blurry', digit=5)
    blurry_image.save(os.path.join(edge_cases_dir, "blurry.png"))
    
    # 回転した画像
    rotated_image = create_edge_case_image('rotated', digit=7)
    rotated_image.save(os.path.join(edge_cases_dir, "rotated.png"))
    
    # ノイズの多い画像
    noisy_image = create_edge_case_image('noisy', digit=3)
    noisy_image.save(os.path.join(edge_cases_dir, "noisy.png"))
    
    # 無効画像を生成
    print("無効画像を生成中...")
    invalid_dir = os.path.join(base_dir, "invalid")
    
    # 数字以外の文字
    not_digit_image = create_invalid_image('not_digit')
    not_digit_image.save(os.path.join(invalid_dir, "not_a_digit.png"))
    
    # 複数の数字
    multiple_digits_image = create_invalid_image('multiple_digits')
    multiple_digits_image.save(os.path.join(invalid_dir, "multiple_digits.png"))
    
    print("すべてのテスト画像が生成されました！")
    print(f"生成された画像:")
    print(f"- 基本数字: {digits_dir}/")
    print(f"- エッジケース: {edge_cases_dir}/")
    print(f"- 無効画像: {invalid_dir}/")

if __name__ == "__main__":
    main()