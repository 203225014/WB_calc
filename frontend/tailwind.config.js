/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'wb-dark': '#0e0e11',
        'wb-accent': '#7300ffff',
        'wb-accent-alt': '#7fffbf',
        'wb-light': '#e9e9ec',
        'wb-box': '#1a1a1f',
        'wb-input': '#111',
      }
    },
  },
  plugins: [],
}