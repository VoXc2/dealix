import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Dealix brand palette
        dealix: {
          navy:    "#001F3F",
          gold:    "#D4AF37",
          black:   "#0A0A0A",
          slate:   "#364558",
          ocean:   "#0066FF",
          emerald: "#10B981",
          coral:   "#EF4444",
          amber:   "#F59E0B",
          light:   "#F3F4F6",
        },
      },
      fontFamily: {
        display: ["Poppins", "Cairo", "system-ui", "sans-serif"],
        body:    ["Inter",   "Tajawal", "system-ui", "sans-serif"],
        mono:    ["IBM Plex Mono", "monospace"],
        sans:    ["Inter",   "Tajawal", "system-ui", "sans-serif"],
      },
      borderRadius: {
        "4xl": "2rem",
        "5xl": "2.5rem",
      },
      boxShadow: {
        gold:  "0 0 28px rgba(212,175,55,0.30)",
        navy:  "0 8px 32px rgba(0,31,63,0.25)",
      },
    },
  },
  plugins: [],
};

export default config;
