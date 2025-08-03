module.exports = {
  // Node.js用のESLint設定です
  env: {
    node: true,       // Node.js環境での実行を想定
    es2021: true,     // ES2021の機能を使用可能
    commonjs: true    // CommonJSモジュールシステムを使用
  },
  extends: [
    'eslint:recommended'  // ESLintの推奨ルール
  ],
  parserOptions: {
    ecmaVersion: 'latest',  // 最新のECMAScriptバージョンを使用
    sourceType: 'module'    // ES6モジュールを使用
  },
  rules: {
    // Node.js開発での品質向上ルールです
    'no-unused-vars': ['error', { argsIgnorePattern: '^_' }], // 未使用変数をエラー
    'no-console': 'off',                 // サーバーサイドではconsole.logを許可
    'prefer-const': 'error',             // letの代わりにconstを推奨
    'no-var': 'error',                   // varの使用を禁止
    'eqeqeq': 'error',                   // 厳密等価演算子（===）を強制
    'curly': 'error',                    // if文などで波括弧を強制
    'no-duplicate-imports': 'error',     // 重複したimportを禁止
    'no-multiple-empty-lines': ['error', { max: 1 }], // 空行の連続を制限
    'no-trailing-spaces': 'error',       // 行末の空白を禁止
    'comma-dangle': ['error', 'never'],  // 末尾のカンマを禁止
    'quotes': ['error', 'single'],       // シングルクォートを強制
    'semi': ['error', 'always']          // セミコロンを強制
  }
};