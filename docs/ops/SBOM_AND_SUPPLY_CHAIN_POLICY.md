# Dealix SBOM and Supply-Chain Policy

Dealix should maintain a Software Bill of Materials for production releases so operators can understand dependencies, licenses, and vulnerability exposure.

## Why SBOM matters

An SBOM is a machine-readable inventory of the software components used by a system. It helps with vulnerability response, license review, supplier transparency, and incident investigation.

## Required release artifacts

For production releases, capture:

- Python dependency inventory.
- Web dependency inventory.
- Container image digest when deployed.
- Git commit SHA.
- Release notes or changelog entry.
- Known high/critical vulnerability disposition.

## Minimum manual commands

Python inventory:

```bash
python -m pip freeze > sbom-python-freeze.txt
```

Web inventory after lockfile exists:

```bash
cd apps/web
npm ci
npm ls --all --json > ../../sbom-web-npm-ls.json
```

Container image metadata:

```bash
docker image inspect dealix:latest > sbom-container-image.json
```

## Review gate

Before production release:

- [ ] Dependency inventories generated.
- [ ] Critical/high findings are fixed or risk-accepted.
- [ ] Runtime image digest is recorded.
- [ ] New dependencies are justified.
- [ ] Public security claims match actual controls.

## Arabic summary

SBOM يساعدك تعرف مكونات النظام والثغرات والتراخيص. قبل أي إطلاق إنتاجي، سجّل اعتماديات Python والواجهة، وراجع الثغرات العالية/الحرجة، واحفظ commit SHA وimage digest.
