# Meta Asset Reconciliation — 2026-09-08

Purpose: avoid creating a third Meta business/app/WABA before existing Dealix-owned assets are inspected in the live Meta account.

## Evidence recovered from founder Gmail

Historical Meta messages from 2026-03-27/28 prove that this Meta identity already existed:

```text
Business name: Revix Solutions
Business ID: 1631530437974003
Business email: sami.assiri11@gmail.com
```

Two Meta Developer apps named Dealix were also referenced:

```text
Dealix App ID: 2598459787207429
Dealix App ID: 1122931886640996
```

The current Meta Business Settings screenshots show a different portfolio named `Portfolio Sami` with no WhatsApp accounts attached. Therefore the absence of a WABA in `Portfolio Sami` does **not** prove that no relevant historical Meta business/app asset exists.

## Required live reconciliation before creating new Meta assets

Founder/account-owner action in Meta UI:

1. Open Meta Business Settings and switch portfolios/businesses.
2. Look specifically for Business ID `1631530437974003` / `Revix Solutions`.
3. Inspect **Accounts -> WhatsApp accounts** under that business.
4. Inspect Meta for Developers for both existing Dealix app IDs.
5. For each app, record only non-secret state:
   - app exists / inaccessible / deleted;
   - owning business portfolio;
   - WhatsApp product added or not;
   - live/development mode;
   - WABA IDs attached, if any;
   - phone-number IDs attached, if any;
   - webhook subscription state;
   - system-user/permission posture without copying tokens.
6. If one existing app is the correct canonical owner, reuse it instead of creating another app.
7. If both apps are stale/duplicate, select one canonical app and retire/archive the duplicate only under an exact action-bound cleanup decision.
8. Create a new WABA/app only when live inspection proves there is no suitable existing canonical asset.

## Selection rule

Preferred canonical Meta structure:

```text
ONE business portfolio
ONE canonical Dealix Meta app
ONE canonical WABA
ONE primary production WhatsApp number
ONE webhook -> api.dealix.me/api/v1/webhooks/whatsapp
```

Do not create parallel WABAs/apps merely because the currently selected portfolio is empty.

## Coexistence decision

If the number currently used on the phone is already an established **WhatsApp Business App** number and Meta's live onboarding flow offers official Business App / Business Platform coexistence for that exact account, evaluate coexistence before full migration. If coexistence is not offered or the number is on ordinary WhatsApp Messenger, prefer the dedicated Dealix business number / standard Meta Cloud API path.

GREEN-API remains transitional and must not become the permanent authority merely because it can link the handset quickly.

## No production effects

This reconciliation document does not:

```text
create/delete a Meta app
create/delete a WABA
move a phone number
change business ownership
rotate secrets
configure a production webhook
enable external send
```
