#!/usr/bin/env bash
# scripts/setup_aws_backup.sh
# One-shot provisioning of the S3 bucket + IAM user for hourly DB backups.
# Idempotent: safe to run multiple times.
#
# Required: AWS CLI configured locally with an admin role.
# Region: me-south-1 (Bahrain) for KSA data residency proximity.
#
# What it creates:
#   - S3 bucket: dealix-backups-ksa (configurable via BUCKET env)
#   - Bucket policy: SSE-S3 default encryption, versioning ON
#   - Lifecycle: STANDARD_IA after 1 day -> GLACIER_IR after 7 days -> DELETE after 30 days
#   - IAM user: dealix-backup-writer with minimal write-only policy
#   - Access key pair printed once at the end — SAVE IMMEDIATELY in 1Password

set -euo pipefail
log() { echo "[setup_aws] $*"; }

BUCKET="${BUCKET:-dealix-backups-ksa}"
REGION="${REGION:-me-south-1}"
IAM_USER="${IAM_USER:-dealix-backup-writer}"

command -v aws >/dev/null || { echo "aws CLI required"; exit 2; }
aws sts get-caller-identity --output text >/dev/null || { echo "aws not authed"; exit 2; }

# 1. Create bucket
if aws s3api head-bucket --bucket "$BUCKET" 2>/dev/null; then
  log "bucket $BUCKET already exists"
else
  log "creating bucket $BUCKET in $REGION"
  aws s3api create-bucket \
    --bucket "$BUCKET" \
    --region "$REGION" \
    --create-bucket-configuration LocationConstraint="$REGION"
fi

# 2. Block public access
log "blocking public access"
aws s3api put-public-access-block --bucket "$BUCKET" \
  --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

# 3. Versioning + default encryption
log "enabling versioning + SSE-S3 encryption"
aws s3api put-bucket-versioning --bucket "$BUCKET" \
  --versioning-configuration Status=Enabled

aws s3api put-bucket-encryption --bucket "$BUCKET" --server-side-encryption-configuration '{
  "Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}, "BucketKeyEnabled": true}]
}'

# 4. Lifecycle
log "applying lifecycle (IA@1d -> Glacier@7d -> expire@30d)"
aws s3api put-bucket-lifecycle-configuration --bucket "$BUCKET" --lifecycle-configuration '{
  "Rules": [{
    "ID": "dealix-hourly-lifecycle",
    "Status": "Enabled",
    "Filter": {"Prefix": "dealix/hourly/"},
    "Transitions": [
      {"Days": 1, "StorageClass": "STANDARD_IA"},
      {"Days": 7, "StorageClass": "GLACIER_IR"}
    ],
    "Expiration": {"Days": 30},
    "NoncurrentVersionExpiration": {"NoncurrentDays": 30}
  }, {
    "ID": "dealix-weekly-cold",
    "Status": "Enabled",
    "Filter": {"Prefix": "dealix/weekly/"},
    "Transitions": [{"Days": 1, "StorageClass": "GLACIER"}],
    "Expiration": {"Days": 365}
  }]
}'

# 5. IAM user + minimal policy
if aws iam get-user --user-name "$IAM_USER" >/dev/null 2>&1; then
  log "IAM user $IAM_USER already exists"
else
  log "creating IAM user $IAM_USER"
  aws iam create-user --user-name "$IAM_USER"
fi

POLICY_DOC=$(cat <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "WriteOnlyToBackupBucket",
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:PutObjectAcl", "s3:AbortMultipartUpload"],
      "Resource": "arn:aws:s3:::${BUCKET}/dealix/*"
    },
    {
      "Sid": "ListOwnBucket",
      "Effect": "Allow",
      "Action": ["s3:ListBucket", "s3:GetBucketLocation"],
      "Resource": "arn:aws:s3:::${BUCKET}"
    }
  ]
}
EOF
)
echo "$POLICY_DOC" > /tmp/dealix-backup-policy.json
aws iam put-user-policy --user-name "$IAM_USER" \
  --policy-name dealix-backup-write \
  --policy-document file:///tmp/dealix-backup-policy.json
rm -f /tmp/dealix-backup-policy.json

# 6. Create or rotate access key
EXISTING_KEYS=$(aws iam list-access-keys --user-name "$IAM_USER" --query 'AccessKeyMetadata[*].AccessKeyId' --output text)
if [[ -n "$EXISTING_KEYS" ]]; then
  log "WARNING: $IAM_USER already has access keys: $EXISTING_KEYS"
  log "skipping key creation. To rotate: aws iam delete-access-key --user-name $IAM_USER --access-key-id <id>"
else
  log "creating access key (PRINTED ONCE — store in 1Password immediately)"
  aws iam create-access-key --user-name "$IAM_USER" --output json
fi

cat <<EOF

──────────────────────────────────────────────────────────────
✓ AWS backup infrastructure ready

Now set these env vars in Railway production:
  BACKUP_S3_BUCKET=$BUCKET
  BACKUP_S3_PREFIX=dealix/hourly
  AWS_DEFAULT_REGION=$REGION
  AWS_ACCESS_KEY_ID=<from output above>
  AWS_SECRET_ACCESS_KEY=<from output above>
  BACKUP_ENCRYPTION_KEY=\$(python -c "import secrets; print(secrets.token_hex(32))")
                       # ^ store in 1Password — also add to Railway

Then schedule the cron in Railway (or wherever your cron worker runs):
  0 * * * *  /app/scripts/hourly_backup.sh >> /var/log/dealix-backup.log 2>&1

Verify with a one-off run:
  bash scripts/hourly_backup.sh
──────────────────────────────────────────────────────────────
EOF
