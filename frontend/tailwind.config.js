/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#08111f",
        mist: "#edf4ff",
        coral: "#ff7a59",
        teal: "#4ad7c3",
        gold: "#f7b500"
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Manrope'", "sans-serif"]
      },
      boxShadow: {
        panel: "0 24px 60px rgba(8, 17, 31, 0.16)"
      }
    }
  },
  plugins: []
};
