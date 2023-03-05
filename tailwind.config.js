module.exports = {
  mode: 'jit',
  purge: [
    './templates/**/*.html',
    './static/**/*.js',
    './static/**/*.css',
  ],
  darkMode: true, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
