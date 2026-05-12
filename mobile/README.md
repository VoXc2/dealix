# Dealix mobile — Expo skeleton

Read-only mobile companion. Approvals, status, and read paths for the
top-3 workflows. Full CRUD lands in v0.2.

## Quick start

```bash
cd mobile
npm install
npx expo start
```

## Deploy

We use **Expo EAS** for store builds; the founder owns the Expo
organisation. CI doesn't auto-publish — releases are tagged
manually after the v0.2 features land.

## Env

`EXPO_PUBLIC_API_BASE` — points at the live Dealix API.
Default: `https://api.dealix.me`.

## What's out of scope here

- Push notifications (handled by Knock-via-Expo Push API later).
- Offline cache.
- Full deal CRUD.
- iOS App Store + Google Play submission.
