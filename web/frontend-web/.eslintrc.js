module.exports = {
    'env': {
        'browser': true,
        'es6': true,
        "node": true
    },
    'extends': [
        'eslint:recommended',
        'plugin:vue/essential'
    ],
    'globals': {
        'Atomics': 'readonly',
        'SharedArrayBuffer': 'readonly'
    },
    'parserOptions': {
        'ecmaVersion': 2018,
        'sourceType': 'module'
    },
    'plugins': [
        'vue'
    ],
    'rules': {
        'indent': [
            'off',
            {}
        ],
        'linebreak-style': [
            'off',
            {}
        ],
        'quotes': [
            'off',
            {}
        ],
        'semi': [
            'off',
            {}
        ],
        // 'indent': [
        //     'off',
        //     2
        // ],
        // 'linebreak-style': [
        //     'error',
        //     'unix'
        // ],
        // 'quotes': [
        //     'error',
        //     'single'
        // ],
        // 'semi': [
        //     'error',
        //     'always'
        // ],
        // "no-unused-vars": "off",
        "vue/script-setup-uses-vars": "off"
    },
    "parserOptions": {
        "parse": "vue-eslint-parser"
    }
};