import os

def w(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ تم إنشاء: {path}")

# 1. ملف package.json (قلب المشروع)
w('frontend/package.json', '''{
  "name": "dealix-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "14.2.15",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "axios": "^1.7.7",
    "lucide-react": "^0.447.0",
    "tailwind-merge": "^2.5.2"
  },
  "devDependencies": {
    "typescript": "^5.6.2",
    "@types/node": "^22.5.4",
    "tailwindcss": "^3.4.12",
    "postcss": "^8.4.45",
    "autoprefixer": "^10.4.20"
  }
}''')

# 2. ملف next.config.js
w('frontend/next.config.js', '''/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
};
module.exports = nextConfig;''')

# 3. ملف tailwind.config.js
w('frontend/tailwind.config.js', '''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: { extend: {} },
  plugins: [],
}''')

# 4. ملف tsconfig.json
w('frontend/tsconfig.json', '''{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}''')
