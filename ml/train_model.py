#!/usr/bin/env python3
"""
MNISTデータセットで数字認識用のSVMモデルを訓練するスクリプト。
このスクリプトはMNISTデータをダウンロードし、SVM分類器を訓練し、モデルを保存します。

新人エンジニア向け解説：
- MNISTは手書き数字のデータセットです
- SVM（Support Vector Machine）は機械学習の分類アルゴリズムです
- このスクリプトは訓練フェーズで、一度だけ実行するものです
"""

# 必要なライブラリをインポート
import numpy as np                        # 数値計算ライブラリ
from sklearn import datasets, svm, metrics  # scikit-learn機械学習ライブラリ
from sklearn.model_selection import train_test_split  # データ分割用
import joblib                             # モデル保存用
import sys                                # システム操作用
import os                                 # ファイル操作用
import ssl                                # SSL設定用
import certifi                            # CA証明書用
import urllib.request                     # SSL設定のため

def configure_ssl():
    """
    SSL証明書の設定を行う関数。
    macOS環境でのSSL証明書エラーを解決します。
    """
    try:
        # 環境変数からSSL設定を確認
        if not os.environ.get('SSL_CERT_FILE') and not os.environ.get('REQUESTS_CA_BUNDLE'):
            # certifiライブラリのCA証明書バンドルを使用
            ca_bundle_path = certifi.where()
            os.environ['SSL_CERT_FILE'] = ca_bundle_path
            os.environ['REQUESTS_CA_BUNDLE'] = ca_bundle_path
            print(f"SSL証明書パスを設定しました: {ca_bundle_path}")
        
        # HTTPSコンテキストを適切に設定
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        
        # urllib用のHTTPSハンドラーを設定
        https_handler = urllib.request.HTTPSHandler(context=ssl_context)
        opener = urllib.request.build_opener(https_handler)
        urllib.request.install_opener(opener)
        
        print("SSL設定が完了しました。")
        return True
        
    except Exception as e:
        print(f"SSL設定中にエラーが発生しました: {e}")
        print("フォールバック: SSL証明書検証を無効化します...")
        
        # 最後の手段としてSSL検証を無効化
        ssl._create_default_https_context = ssl._create_unverified_context
        print("警告: SSL証明書検証が無効化されました。")
        return False

def train_svm_model():
    """
    MNISTデータセットでSVMモデルを訓練し、保存する関数。
    
    新人エンジニア向け解説：
    1. MNISTデータをダウンロード
    2. データを訓練用と検証用に分割
    3. データを正規化（ピクセル値を0-1の範囲に）
    4. SVMモデルを訓練
    5. モデルの性能を評価
    6. モデルをファイルに保存
    """
    
    # SSL設定を最初に実行
    print("SSL設定を確認中...")
    ssl_configured = configure_ssl()
    
    print("MNISTデータセットを読み込み中...")
    # scikit-learnからMNISTデータセットを読み込み
    # MNISTは70,000枚の手書き数字画像のデータセット
    try:
        mnist = datasets.fetch_openml('mnist_784', version=1, as_frame=False, parser='liac-arff')
    except Exception as e:
        if "SSL" in str(e) or "certificate" in str(e):
            print(f"SSL証明書エラーが発生しました: {e}")
            print("代替方法を試行中...")
            
            # 再度SSL設定を試行（無効化含む）
            if ssl_configured:
                print("SSL検証を無効化して再試行します...")
                ssl._create_default_https_context = ssl._create_unverified_context
            
            try:
                mnist = datasets.fetch_openml('mnist_784', version=1, as_frame=False, parser='liac-arff')
                print("代替方法でデータセットの取得に成功しました。")
            except Exception as e2:
                print(f"データセット取得に失敗しました: {e2}")
                print("\n解決策:")
                print("1. インターネット接続を確認してください")
                print("2. Python証明書を更新してください:")
                print("   /Applications/Python\\ 3.13/Install\\ Certificates.command")
                print("3. 環境変数を設定してください:")
                print("   export SSL_CERT_FILE=$(python -c 'import certifi; print(certifi.where())')")
                raise e2
        else:
            raise e
    
    # 特徴量（ピクセル値）とラベル（正解の数字）を取得
    X, y = mnist.data, mnist.target.astype(int)
    
    # 高速な訓練のためにサブセットを使用（最初の10,000サンプル）
    # 精度を上げたい場合はこの数値を増やすことができます
    X_subset = X[:10000]
    y_subset = y[:10000]
    
    # データを訓練用と検証用に分割（訓練用：80%、検証用：20%）
    X_train, X_val, y_train, y_val = train_test_split(
        X_subset, y_subset, test_size=0.2, random_state=42
    )
    
    print(f"訓練データセットサイズ: {len(X_train)}")
    print(f"検証データセットサイズ: {len(X_val)}")
    
    # ピクセル値を0-1の範囲に正規化（元々は0-255の範囲）
    # これにより機械学習モデルの訓練が安定します
    X_train = X_train / 255.0
    X_val = X_val / 255.0
    
    print("SVMモデルを訓練中...")
    # RBFカーネルを使用したSVM分類器を作成
    # RBFカーネルは非線形データに対して有効です
    clf = svm.SVC(kernel='rbf', gamma='scale', C=10, random_state=42)
    
    # モデルを訓練します。この処理には数分かかることがあります
    clf.fit(X_train, y_train)
    
    # 検証データでモデルの性能を評価
    y_pred = clf.predict(X_val)
    accuracy = metrics.accuracy_score(y_val, y_pred)
    
    print(f"検証精度: {accuracy:.4f}")
    print("分類レポート:")
    print(metrics.classification_report(y_val, y_pred))
    
    # 訓練したモデルをファイルに保存
    model_path = os.path.join(os.path.dirname(__file__), 'svm_model.pkl')
    joblib.dump(clf, model_path)
    print(f"モデルを保存しました: {model_path}")
    
    return clf, accuracy

# メイン処理：スクリプトが直接実行された場合のみ実行されます
if __name__ == "__main__":
    try:
        # モデル訓練を実行
        model, accuracy = train_svm_model()
        print(f"訓練が成功しました！ 最終精度: {accuracy:.4f}")
    except Exception as e:
        # エラーが発生した場合の処理
        print(f"訓練中にエラーが発生しました: {e}")
        sys.exit(1)  # エラーコードで1で終了