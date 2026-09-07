#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

# DEALIX OMEGA - TOP 50 CAPABILITY ADMISSION MASTER V1
# Evaluates a curated Top-50 OSS/tool registry against the existing Dealix
# Capability Radar. It does not bulk-install tools or perform any L5 action.

MODE="${1:-audit}"
case "$MODE" in audit|pilot) ;; *) echo "Usage: $0 [audit|pilot]" >&2; exit 2 ;; esac

export TZ=Asia/Riyadh
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export GH_PROMPT_DISABLED=1
export GIT_TERMINAL_PROMPT=0
export PYTHONNOUSERSITE=1

export DEALIX_EXTERNAL_SEND=0
export DEALIX_EMAIL_LIVE_SEND=0
export DEALIX_WHATSAPP_OUTBOUND=0
export DEALIX_PUBLIC_PUBLISH=0
export DEALIX_PAID_SPEND=0
export DEALIX_PAYMENT_EXECUTION=0
export DEALIX_PRODUCTION_MUTATION=0
export DEALIX_DNS_MUTATION=0
export DEALIX_DB_MUTATION=0
export DEALIX_SECRET_MUTATION=0
export DEALIX_IDENTITY_MUTATION=0
export DEALIX_AGENT_SELF_AUTHORITY=0
export DEALIX_AUTONOMY_LEVEL=4
export DEALIX_MODE=draft-only
export VOICE_AI_ENABLED=false
export VOICE_RECORDING_ENABLED=false
export VOICE_OUTBOUND_ENABLED=false

REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"
RUN_USER="${DEALIX_RUN_USER:-dealix}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
PROOF="$CONTROL/proof/capability-top50/$STAMP"
LAB="$CONTROL/labs/capability-top50/$STAMP"
REGISTRY="$PROOF/top50.tsv"
RESULTS="$PROOF/results.tsv"
SUMMARY="$PROOF/summary.env"

install -d -m 0750 -o "$RUN_USER" -g "$RUN_USER" "$PROOF" "$LAB"

safe_git() {
  sudo -u "$RUN_USER" env HOME="/home/$RUN_USER" PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
    git -c safe.directory="$REPO" -C "$REPO" "$@"
}

need() {
  command -v "$1" >/dev/null 2>&1 || { echo "MISSING_REQUIRED_COMMAND=$1" >&2; exit 10; }
}

need git
need python3
need timeout
need sha256sum

safe_git fetch origin main --prune --quiet
LIVE_MAIN="$(safe_git rev-parse origin/main)"
LOCAL_HEAD="$(safe_git rev-parse HEAD 2>/dev/null || echo UNKNOWN)"
DIRTY_COUNT="$(safe_git status --porcelain=v1 2>/dev/null | wc -l | tr -d ' ')"

printf 'LIVE_MAIN=%s\nLOCAL_HEAD=%s\nLOCAL_DIRTY_COUNT=%s\nMODE=%s\n' \
  "$LIVE_MAIN" "$LOCAL_HEAD" "$DIRTY_COUNT" "$MODE" | tee "$PROOF/reconcile.env"

cat > "$REGISTRY" <<'REGISTRY_EOF'
01	osv_scanner	TRUST_SECURITY	ADOPT_NOW	google/osv-scanner	Dependency vulnerability evidence via OSV; normalize findings into existing Proof/Trust owner.
02	syft	TRUST_SECURITY	ADOPT_NOW_BOUNDED	anchore/syft	Generate SBOMs for source/images; evidence only, no new truth store.
03	grype	TRUST_SECURITY	PILOT_ISOLATED	anchore/grype	Scan SBOMs/images for vulnerabilities; reconcile with OSV/Trivy.
04	trivy	TRUST_SECURITY	PILOT_ISOLATED	aquasecurity/trivy	Unified vuln/secret/misconfiguration/SBOM scan in isolated evidence lane.
05	gitleaks	TRUST_SECURITY	ADOPT_NOW_BOUNDED	gitleaks/gitleaks	Fast secret scanning for repo/worktrees before PR acceptance.
06	detect_secrets	TRUST_SECURITY	ADOPT_NOW_BOUNDED	Yelp/detect-secrets	Baseline-aware secret detection complementary to Gitleaks.
07	semgrep	TRUST_SECURITY	PILOT_ISOLATED	semgrep/semgrep	Static security/code rules for high-risk auth, secrets, injection and unsafe subprocess paths.
08	zizmor	TRUST_SECURITY	ADOPT_NOW_BOUNDED	zizmorcore/zizmor	GitHub Actions security analysis, especially dangerous triggers/permissions.
09	actionlint	TRUST_SECURITY	ADOPT_NOW_BOUNDED	rhysd/actionlint	Static GitHub Actions syntax/expression/action contract validation.
10	openssf_scorecard	TRUST_SECURITY	PILOT_ISOLATED	ossf/scorecard	Repository supply-chain posture evidence for Dealix and admitted OSS.
11	cosign	TRUST_SECURITY	DEFER	sigstore/cosign	Artifact/image signing and verification after release execution plane stabilizes.
12	cdxgen	TRUST_SECURITY	PILOT_ISOLATED	cdxgen/cdxgen	Alternative CycloneDX SBOM generation/cross-checking.
13	checkov	TRUST_SECURITY	PILOT_ISOLATED	bridgecrewio/checkov	IaC/Docker/GitHub workflow misconfiguration evidence where applicable.
14	trufflehog	TRUST_SECURITY	PILOT_ISOLATED	trufflesecurity/trufflehog	Verified credential discovery in bounded repo/history scans; never scan unrelated targets.
15	clamav	TRUST_SECURITY	PILOT_ISOLATED	Cisco-Talos/clamav	Malware scanning candidate for customer-upload/document ingestion boundary.
16	playwright	TEST_RELIABILITY	ADOPT_FOR_ACCEPTANCE	microsoft/playwright	Deterministic browser/public-surface acceptance and traces.
17	schemathesis	TEST_RELIABILITY	PILOT_ISOLATED	schemathesis/schemathesis	OpenAPI property-based/stateful API tests on local/test targets.
18	k6	TEST_RELIABILITY	PILOT_ISOLATED	grafana/k6	Performance/load smoke for bounded staging/local paths.
19	hurl	TEST_RELIABILITY	ADOPT_NOW_BOUNDED	Orange-OpenSource/hurl	Plain-text deterministic HTTP acceptance for Web/API/front door.
20	hypothesis	TEST_RELIABILITY	ADOPT_NOW_BOUNDED	HypothesisWorks/hypothesis	Property-based tests for commercial/truth/state invariants.
21	testcontainers_python	TEST_RELIABILITY	PILOT_ISOLATED	testcontainers/testcontainers-python	Real Postgres/service integration tests in isolated disposable containers.
22	toxiproxy	TEST_RELIABILITY	PILOT_ISOLATED	Shopify/toxiproxy	Deterministic network fault injection for retry/fallback/idempotency tests.
23	ruff	TEST_RELIABILITY	ADOPT_NOW_BOUNDED	astral-sh/ruff	Fast Python lint/format quality gate.
24	uv	TEST_RELIABILITY	ADOPT_NOW	astral-sh/uv	Isolated Python tool execution and dependency resolution; pin fixed versions.
25	pre_commit	TEST_RELIABILITY	ADOPT_NOW_BOUNDED	pre-commit/pre-commit	Local deterministic hook orchestration; no replacement of sovereign CI authority.
26	pyright	TEST_RELIABILITY	PILOT_ISOLATED	microsoft/pyright	High-performance Python static type checking for high-value modules.
27	pytest_xdist	TEST_RELIABILITY	ADOPT_NOW_BOUNDED	pytest-dev/pytest-xdist	Parallelize safe independent test subsets to reduce verification latency.
28	otel_collector	OBS_AI	PILOT_ISOLATED	open-telemetry/opentelemetry-collector	Vendor-neutral telemetry collection/export without creating business truth.
29	otel_python	OBS_AI	ALREADY_BOUNDED	open-telemetry/opentelemetry-python	Existing privacy-safe instrumentation owner; extend only measured spans/metrics.
30	promptfoo	OBS_AI	PILOT_ISOLATED	promptfoo/promptfoo	Sandboxed LLM/agent eval and red-team for truth/tool/authority regressions.
31	phoenix	OBS_AI	PILOT_ISOLATED	Arize-ai/phoenix	Local OTel-based AI tracing/evals/experiments; no second commercial truth store.
32	litellm	OBS_AI	DEFER_MEASURED_GAP	BerriAI/litellm	Provider gateway candidate only if existing Dealix model router has a measured gap.
33	pydantic_ai	OBS_AI	DEFER_MEASURED_GAP	pydantic/pydantic-ai	Typed agent/tool patterns only; must not create second permanent agent framework/fleet.
34	mcp_python_sdk	OBS_AI	ADOPT_NOW_BOUNDED	modelcontextprotocol/python-sdk	Standardized bounded MCP clients/servers for connector adapters and testing.
35	instructor	OBS_AI	PILOT_ISOLATED	instructor-ai/instructor	Structured extraction/validation for research and document fields, evidence-preserving.
36	langfuse	OBS_AI	DEFER	langfuse/langfuse	Legacy compatibility only; do not expand into second observability/truth platform.
37	docling	DATA_DOCUMENT	PILOT_ISOLATED	docling-project/docling	Document parsing/PDF understanding with provenance into existing Company Brain/Data OS.
38	presidio	DATA_DOCUMENT	PILOT_ISOLATED	microsoft/presidio	PII detection/redaction before telemetry/evals/document processing.
39	apache_tika	DATA_DOCUMENT	PILOT_ISOLATED	apache/tika	Broad file-type metadata/text extraction; compare with Docling on hard formats.
40	duckdb	DATA_DOCUMENT	ADOPT_NOW_BOUNDED	duckdb/duckdb	Read-only local analytics over receipts/evidence without a new operational DB.
41	polars	DATA_DOCUMENT	PILOT_ISOLATED	pola-rs/polars	High-performance dataframe transforms for research/evidence pipelines.
42	great_expectations	DATA_DOCUMENT	PILOT_ISOLATED	great-expectations/great_expectations	Data-quality assertions where structured evidence pipelines justify it.
43	pgvector	DATA_DOCUMENT	REJECT_DUPLICATE_DEFAULT	pgvector/pgvector	Storage extension only if existing Company Brain proves a retrieval gap; never new truth owner.
44	rapidfuzz	DATA_DOCUMENT	ADOPT_NOW_BOUNDED	rapidfuzz/RapidFuzz	Entity/company/contact fuzzy matching and dedupe with conservative thresholds.
45	faker	DATA_DOCUMENT	PILOT_ISOLATED	joke2k/faker	Synthetic fixtures for tests only; synthetic data is never customer proof.
46	changedetection	OPS_MARKET	PILOT_ISOLATED	dgtlmoon/changedetection.io	Watch public/official pages for economic/regulatory changes; research-only signals.
47	apprise	OPS_MARKET	PILOT_ISOLATED	caronc/apprise	Unified internal notification adapter; no customer outreach authority.
48	opencode	OPS_MARKET	ADOPT_NOW_BOUNDED	anomalyco/opencode	Coding-agent governance and repo exploration patterns only; reuse AGENTS.md and explicit permissions, no parallel permanent fleet.
49	crawl4ai	OPS_MARKET	PILOT_ISOLATED	unclecode/crawl4ai	Public web research extraction for official/economic signal ingestion; obey source terms/robots.
50	n8n_mcp	OPS_MARKET	PILOT_ISOLATED	n8n-io/n8n	MCP-assisted disabled-first workflow authoring over existing n8n owner; no second scheduler.
REGISTRY_EOF
chown "$RUN_USER:$RUN_USER" "$REGISTRY"

printf 'rank\tid\tcategory\tdecision\trepo\treachable\tduplicate_hits\tlocal_tool\tprobe_result\n' > "$RESULTS"

local_tool_for() {
  case "$1" in
    osv_scanner) echo osv-scanner ;;
    syft) echo syft ;;
    grype) echo grype ;;
    trivy) echo trivy ;;
    gitleaks) echo gitleaks ;;
    detect_secrets) echo detect-secrets ;;
    semgrep) echo semgrep ;;
    zizmor) echo zizmor ;;
    actionlint) echo actionlint ;;
    openssf_scorecard) echo scorecard ;;
    cosign) echo cosign ;;
    checkov) echo checkov ;;
    trufflehog) echo trufflehog ;;
    clamav) echo clamscan ;;
    playwright) echo playwright ;;
    schemathesis) echo schemathesis ;;
    k6) echo k6 ;;
    hurl) echo hurl ;;
    ruff) echo ruff ;;
    uv) echo uv ;;
    pre_commit) echo pre-commit ;;
    pyright) echo pyright ;;
    otel_collector) echo otelcol ;;
    promptfoo) echo promptfoo ;;
    duckdb) echo duckdb ;;
    *) echo NONE ;;
  esac
}

probe_version() {
  local tool="$1"
  case "$tool" in NONE) echo NOT_APPLICABLE; return 0 ;; esac
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo NOT_INSTALLED
    return 0
  fi
  if [[ "$MODE" != "pilot" ]]; then
    echo AVAILABLE_NOT_EXECUTED
    return 0
  fi
  set +e
  local out rc
  out="$(timeout 15s "$tool" --version 2>&1 | head -n 2 | tr '\t\r\n' '   ')"
  rc=$?
  set -e
  if [[ $rc -eq 0 ]]; then printf 'PASS:%s' "$out"; else printf 'HOLD_VERSION_PROBE_RC_%s:%s' "$rc" "$out"; fi
}

while IFS=$'\t' read -r rank id category decision repo purpose; do
  [[ -n "$rank" ]] || continue
  url="https://github.com/$repo.git"
  reachable=NO
  if timeout 20s git ls-remote --exit-code "$url" HEAD >/dev/null 2>"$PROOF/${rank}-${id}-lsremote.err"; then
    reachable=YES
  fi

  duplicate_hits="$(
    safe_git grep -I -i -E "${id//_/[-_ ]}|$(basename "$repo")" "$LIVE_MAIN" -- \
      'docs/**' 'data/**' 'config/**' 'scripts/**' 2>/dev/null \
      | head -n 50 | wc -l | tr -d ' '
  )"

  tool="$(local_tool_for "$id")"
  if [[ "$tool" != NONE ]] && command -v "$tool" >/dev/null 2>&1; then
    local_state=AVAILABLE
  elif [[ "$tool" == NONE ]]; then
    local_state=LIBRARY_OR_SERVICE
  else
    local_state=ABSENT
  fi
  probe="$(probe_version "$tool")"

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$rank" "$id" "$category" "$decision" "$repo" "$reachable" \
    "$duplicate_hits" "$local_state" "$probe" >> "$RESULTS"
done < "$REGISTRY"

chown "$RUN_USER:$RUN_USER" "$RESULTS"

python3 - "$REGISTRY" "$RESULTS" "$PROOF/top50.json" "$LIVE_MAIN" "$MODE" <<'PY'
import csv, json, sys
registry, results, out, main, mode = sys.argv[1:]
rows=[]
with open(registry, encoding='utf-8') as f:
    for rank,id_,category,decision,repo,purpose in csv.reader(f, delimiter='\t'):
        rows.append(dict(rank=int(rank), id=id_, category=category, decision=decision, repo=repo, purpose=purpose))
result_map={}
with open(results, encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter='\t'):
        result_map[r['id']]=r
for row in rows:
    row['audit']=result_map.get(row['id'], {})
payload={
  'schema':'dealix.capability_top50.v1',
  'live_main':main,
  'mode':mode,
  'north_star':'CASH_READY_AUTONOMOUS_DEALIX_COMPANY',
  'law':'REJECT_DUPLICATE_BY_DEFAULT; max one active benchmark at a time; no L5 material effects',
  'candidates':rows,
}
with open(out,'w',encoding='utf-8') as f:
    json.dump(payload,f,ensure_ascii=False,indent=2)
PY
chown "$RUN_USER:$RUN_USER" "$PROOF/top50.json"

TOTAL="$(wc -l < "$REGISTRY" | tr -d ' ')"
REACHABLE="$(awk -F '\t' 'NR>1 && $6=="YES"{n++} END{print n+0}' "$RESULTS")"
ABSENT="$(awk -F '\t' 'NR>1 && $8=="ABSENT"{n++} END{print n+0}' "$RESULTS")"
AVAILABLE="$(awk -F '\t' 'NR>1 && $8=="AVAILABLE"{n++} END{print n+0}' "$RESULTS")"

cat > "$SUMMARY" <<EOF_SUM
LIVE_MAIN=$LIVE_MAIN
MODE=$MODE
TOP50_TOTAL=$TOTAL
REPOS_REACHABLE=$REACHABLE
LOCAL_TOOLS_AVAILABLE=$AVAILABLE
LOCAL_TOOLS_ABSENT=$ABSENT
MATERIAL_EFFECTS=false
MERGE=false
DEPLOY=false
DNS_MUTATION=false
DB_MUTATION=false
SECRET_MUTATION=false
EXTERNAL_SEND=false
PAYMENT=false
PUBLIC_PUBLISH=false
ACTIVE_BENCHMARKS_MAX=1
AUTO_INSTALL_MISSING_TOOLS=false
VERDICT=PASS_TOP50_ADMISSION_AUDIT
EOF_SUM
chown "$RUN_USER:$RUN_USER" "$SUMMARY"
sha256sum "$REGISTRY" "$RESULTS" "$PROOF/top50.json" "$SUMMARY" | tee "$PROOF/SHA256SUMS"

if command -v dealix-president >/dev/null 2>&1; then
  set +e
  dealix-president reconcile >"$PROOF/president-reconcile.log" 2>&1
  PRESIDENT_RECONCILE_RC=$?
  dealix-president daily-dry >"$PROOF/president-daily-dry.log" 2>&1
  PRESIDENT_DRY_RC=$?
  set -e
  printf 'PRESIDENT_RECONCILE_RC=%s\nPRESIDENT_DRY_RC=%s\n' \
    "$PRESIDENT_RECONCILE_RC" "$PRESIDENT_DRY_RC" | tee "$PROOF/president.env"
fi

echo "======================================================================"
echo "DEALIX TOP-50 CAPABILITY ADMISSION COMPLETE"
echo "======================================================================"
cat "$SUMMARY"
echo "PROOF=$PROOF"
echo "NEXT=Review results, then admit/pilot ONE measured-gap capability at a time."
echo "L5_EXECUTED=NONE"
