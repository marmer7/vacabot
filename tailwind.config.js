module.exports = {
  mode: 'jit',
  purge: [
    './app/templates/**/*.html',
    './app/static/**/*.js',
    './app/static/**/*.css',
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
