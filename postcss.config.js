const path = require('path');

module.exports = (ctx) => ({
    plugins: [
        require('tailwindcss')(path.resolve(__dirname, 'tailwind.config.js')),
        require('autoprefixer'),
        ctx.env === 'production' && require('@fullhuman/postcss-purgecss')({
            content: [
                path.resolve(__dirname, 'templates/**/*.html')
            ],
            defaultExtractor: content => content.match(/[A-Za-z0-9-_:/]+/g) || []
        })
    ]
})