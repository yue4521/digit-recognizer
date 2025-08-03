module.exports = {
  // JavaScriptコードの品質をチェックするツール
  env: {
    browser: true,    // ブラウザ環境での実行を想定
    es2021: true,     // ES2021の機能を使用可能
    node: true        // Node.js環境での実行も想定
  },
  extends: [
    'eslint:recommended',           // ESLintの推奨ルール
    'plugin:react/recommended',     // React用の推奨ルール
    'plugin:react-hooks/recommended' // React Hooks用の推奨ルール
  ],
  parserOptions: {
    ecmaFeatures: {
      jsx: true       // JSXの解析を有効化
    },
    ecmaVersion: 'latest',  // 最新のECMAScriptバージョンを使用
    sourceType: 'module'    // ES6モジュールを使用
  },
  plugins: [
    'react',          // Reactプラグイン
    'react-hooks'     // React Hooksプラグイン
  ],
  rules: {
    // 以下はコード品質向上のためのルールです
    'react/prop-types': 'off',           // PropTypesの使用を強制しない
    'react/react-in-jsx-scope': 'off',   // React 17+では不要
    'no-unused-vars': 'warn',            // 未使用変数を警告
    'no-console': 'warn',                // console.logを警告（開発時は有用）
    'prefer-const': 'error',             // letの代わりにconstを推奨
    'no-var': 'error',                   // varの使用を禁止
    'eqeqeq': 'error',                   // 厳密等価演算子（===）を強制
    'curly': 'error',                    // if文などで波括弧を強制
    'no-duplicate-imports': 'error',     // 重複したimportを禁止
    'no-multiple-empty-lines': ['error', { max: 1 }] // 空行の連続を制限
  },
  settings: {
    react: {
      version: 'detect'  // インストールされているReactのバージョンを自動検出
    }
  }
};