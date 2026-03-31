import json
import os

path = 'frontend/package.json'
with open(path, 'r') as f:
    data = json.load(f)

# إضافة clsx للمكتبات الأساسية
data['dependencies']['clsx'] = '^2.1.1'

# إضافة التعريفات الناقصة للـ devDependencies
data['devDependencies']['@types/react'] = '^18.3.5'
data['devDependencies']['@types/react-dom'] = '^18.3.0'
data['devDependencies']['@types/node'] = '^22.5.4'

with open(path, 'w') as f:
    json.dump(data, f, indent=2)

print("✅ تمت إضافة 'clsx' والتعريفات الناقصة لملف package.json")
