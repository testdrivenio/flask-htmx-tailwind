const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
    future: {
        // removeDeprecatedGapUtilities: true,
        // purgeLayersByDefault: true,
    },
    purge: [],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Inter var', ...defaultTheme.fontFamily.sans],
            },
            tableLayout: ['hover', 'focus'],
        },
    },
    variants: {},
    plugins: [
        require('@tailwindcss/ui'),
    ],
}