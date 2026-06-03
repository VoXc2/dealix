# مهام Haiku — أسرع وأرخص 5x من Sonnet

## متى تُفعّل Haiku؟

```bash
/model haiku
```

## قائمة مهام Haiku المثالية

### التنسيق والنظافة
```
[haiku] نسّق هذا الملف باستخدام ruff format
[haiku] أضف trailing commas لكل function calls في clients.py
[haiku] حوّل كل print statements إلى logger.info
[haiku] أزل كل unused imports في api/routes/
```

### إعادة التسمية
```
[haiku] أعد تسمية المتغير `u` إلى `user` في جميع أنحاء auth.py
[haiku] حوّل كل camelCase إلى snake_case في schemas/
[haiku] أعد تسمية الدالة `getData` إلى `get_data`
```

### Boilerplate
```
[haiku] أنشئ __init__.py فارغاً لكل مجلدات api/routes/
[haiku] أضف docstring بسيطة لكل دالة في core/utils.py
[haiku] أضف type hints لمعاملات الدوال في services/client.py
```

### ترجمة رسائل
```
[haiku] ترجم كل رسائل الخطأ في api/routes/clients.py إلى العربية
[haiku] أضف `_ar` version لكل error messages
```

### البحث والاستعلام
```
[haiku] ابحث عن كل استخدامات asyncio.sleep في المشروع
[haiku] أعطني قائمة بكل endpoints في api/routes/
[haiku] كم عدد الملفات في مجلد tests/?
```

## برومبت Haiku المثالي

```
[haiku] [مهمة بسيطة محددة] في [ملف محدد]. No explanations.
```

## العودة إلى Sonnet

```bash
/model sonnet
```

لا تنسَ الرجوع بعد الانتهاء من المهام الميكانيكية.
