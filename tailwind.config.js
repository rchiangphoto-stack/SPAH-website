/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.html"],
  theme: {
    extend: {
      colors: {
        brand:  '#5A7FA6',
        sage:   '#7A9E8E',
        terra:  '#A8673A',
        sky:    '#89A8C4',
        warm:   '#FAFAF8',
        dark:   '#2A3442',
        muted:  '#5C6B7A',
      },
      fontFamily: {
        display: ['"Playfair Display"', 'Georgia', 'serif'],
        body:    ['"Lato"', 'sans-serif'],
      },
    }
  },
  plugins: [],
}
