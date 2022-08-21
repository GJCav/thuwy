module.exports = {
    root: true,
    env: {
        node: true,
    },
    "env": {
        "browser": true,
        "es2021": true
    },
    "extends": [
        'plugin:vue/essential',
        'eslint:recommended'
    ],
    "overrides": [
    ],
    "parserOptions": {
        "sourceType": "module",
        "parser": '@babel/eslint-parser',
        "requireConfigFile": false
    },
    rules: {
        'vue/multi-word-component-names': ['warn', {}],
        'no-unused-vars': ['warn', {}],
        'no-trailing-spaces': ["off", {}],
        "quotes": ['off', {}],
        "quote-props": ["off", {}],
        "comma-dangle": ["off", {}],
        "eol-last": ["off", {}],
        "semi": ["off", {}],
        "no-multiple-empty-lines": ["off", {}],
        "prefer-destructuring": ["warn", {
          "array": false,
          "object": true
        }, {}],
        "padded-blocks": ["off"],
        "no-multi-spaces": ["off"]
    },
}
