// tailwind.config.js
const {colors, spacing, radii, typography} = require('./shared/theme/designTokens');

module.exports = {
    content: [
        './src/**/*.{js,jsx,ts,tsx}',
        // …
    ],
    theme: {
        extend: {
            colors: {
                primary: colors.primary,
                primaryDark: colors.primaryDark,
                secondary: colors.secondary,
                background: colors.background,
                surface: colors.surface,
                text: colors.text,
                textSecondary: colors.textSecondary,
                border: colors.border,
                error: colors.error,
            },
            spacing: {
                xs: spacing.xs,
                sm: spacing.sm,
                md: spacing.md,
                lg: spacing.lg,
                xl: spacing.xl,
            },
            borderRadius: {
                sm: radii.sm,
                md: radii.md,
                lg: radii.lg,
            },
            fontSize: {
                'h1': [typography.h1.fontSize, {lineHeight: typography.h1.lineHeight}],
                'h2': [typography.h2.fontSize, {lineHeight: typography.h2.lineHeight}],
                'body': [typography.body.fontSize, {lineHeight: typography.body.lineHeight}],
                'caption': [typography.caption.fontSize, {lineHeight: typography.caption.lineHeight}],
            },
            fontWeight: {
                'h1': typography.h1.fontWeight,
                'h2': typography.h2.fontWeight,
            }
        }
    },
    plugins: [],
    darkMode: 'class',
}