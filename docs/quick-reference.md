# クイックリファレンス

手書き数字認識アプリの利用可能なスクリプトとパフォーマンス情報です。

## 利用可能なスクリプト

| スクリプト | 説明 |
|-----------|------|
| `npm run setup` | 完全セットアップ（依存関係 + モデル訓練） |
| `npm run dev` | 開発サーバー起動 |
| `npm run build` | 本番ビルド |
| `npm start` | 本番サーバー起動 |
| `npm run train-model` | SVMモデル訓練 |

## パフォーマンス

- **モデル精度**: 約95% (MNISTテストセット)
- **予測時間**: 平均500ms
- **サポート形式**: JPEG, PNG
- **ファイルサイズ制限**: 2MB

## プロジェクト構成

```
digit-recognizer/
├── client/          # Reactフロントエンド
├── server/          # Express.jsバックエンド
├── ml/              # Python機械学習
├── docs/            # ドキュメント
├── venv/            # Python仮想環境
└── package.json     # ルートスクリプト
```

## よくある問題の解決方法

- **モジュールエラー** → `npm run install-all`
- **Pythonエラー** → 仮想環境の確認
- **モデルエラー** → `npm run train-model`
- **ポート競合** → プロセス終了または.env設定

詳細なトラブルシューティングは [troubleshooting.md](troubleshooting.md) を参照してください。