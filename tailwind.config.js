/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#172126",
        panel: "#f7f8f6",
        line: "#d8ded8",
        risk: "#b91c1c",
        amberline: "#b7791f",
        signal: "#0f766e"
      },
      boxShadow: {
        subtle: "0 1px 2px rgba(23,33,38,0.08)"
      }
    }
  },
  plugins: []
};
