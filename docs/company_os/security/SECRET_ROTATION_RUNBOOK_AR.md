# Secret Rotation Runbook

## متى ندوّر الأسرار؟

- إذا ظهر token في chat.
- إذا ظهر token في logs.
- إذا انتقل شخص من الفريق.
- كل 30–90 يوم حسب الحساسية.

## Railway

1. افتح Project Settings / Tokens.
2. احذف token المكشوف.
3. أنشئ token جديد عند الحاجة فقط.
4. لا تحفظه في repo.

## GitHub

1. افتح Developer Settings / Personal Access Tokens.
2. احذف PAT المكشوف.
3. استخدم fine-grained token عند الحاجة.
4. لا تلصقه في chat أو سكربت.

## قاعدة

Secrets لا تدخل Git، ولا markdown، ولا logs، ولا screenshots.
