#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# rotate_secrets.sh — تدوير كل الأسرار (API keys, webhook secrets)
# Generates fresh random secrets and writes them to .env.new.
# يولّد أسراراً عشوائية ويكتبها في .env.new للمراجعة ثم النقل.
# ─────────────────────────────────────────────────────────────
set -euo pipefail

ENV_SRC="${1:-.env}"
ENV_OUT="${2:-.env.new}"

if [[ ! -f "$ENV_SRC" ]]; then
  echo "✗ Source env file not found: $ENV_SRC" >&2
  exit 1
fi

gen() { openssl rand -hex 32; }
gen_b64() { openssl rand -base64 48 | tr -d '\n'; }

timestamp=$(date -u +%Y%m%dT%H%M%SZ)
cp "$ENV_SRC" "${ENV_SRC}.bak.${timestamp}"
echo "✓ Backed up → ${ENV_SRC}.bak.${timestamp}"

# Rotate well-known secrets (skip externally managed ones like STRIPE, ANTHROPIC)
declare -a ROTATE_VARS=(
  "API_KEYS"
  "HUBSPOT_APP_SECRET"
  "CALENDLY_WEBHOOK_SECRET"
  "N8N_WEBHOOK_SECRET"
  "JWT_SECRET"
  "DEALIX_INTERNAL_TOKEN"
)

cp "$ENV_SRC" "$ENV_OUT"
for var in "${ROTATE_VARS[@]}"; do
  new_val=$(gen)
  if grep -q "^${var}=" "$ENV_OUT"; then
    # portable sed (works on GNU + BSD via tmp file)
    tmp=$(mktemp)
    awk -v k="$var" -v v="$new_val" -F= 'BEGIN{done=0} {
      if ($1 == k && !done) { print k"="v; done=1 } else { print }
    }' "$ENV_OUT" > "$tmp"
    mv "$tmp" "$ENV_OUT"
    echo "✓ Rotated $var"
  else
    echo "${var}=${new_val}" >> "$ENV_OUT"
    echo "+ Added $var"
  fi
done

echo ""
echo "✓ New secrets written → $ENV_OUT"
echo "   Review, then: mv $ENV_OUT $ENV_SRC && systemctl restart dealix-api"
echo "   Rollback:     cp ${ENV_SRC}.bak.${timestamp} $ENV_SRC"
