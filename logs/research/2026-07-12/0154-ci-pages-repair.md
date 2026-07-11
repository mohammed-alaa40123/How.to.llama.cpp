# CI and Pages repair

- Run time: 2026-07-12 01:54 Africa/Cairo
- Repository: `mohammed-alaa40123/How.to.llama.cpp`
- Scope: GitHub Actions, Pages deployment, durable TODO/context contract

## Evidence inspected

- Root `README.md` and scheduled-run protocol
- `docs/reference/project-state.md`
- `docs/reference/research-log.md`
- `docs/reference/research-ledger.md`
- All three existing workflow files
- Official `actions/configure-pages` action metadata
- Official GitHub Pages starter workflow

## Verified repair

1. Added an independent `Documentation CI` workflow that validates context, shell/Python scripts, the interactive asset, and a strict MkDocs build.
2. Changed Pages deployment to detect whether Pages is enabled before configuring or uploading an artifact.
3. Upgraded deployment to `actions/deploy-pages@v5`.
4. Added a post-deployment health check that requires HTTP 200 and the project title.
5. Added `scripts/check_site.sh` for manual/local verification.
6. Added the previously omitted interactive HTML asset to the publication set.
7. Added a living README TODO contract and required every scheduled run to maintain it.

## Validation

```text
python3 scripts/validate_project_context.py  -> passed
bash -n scripts/*.sh                        -> passed
python3 -m py_compile scripts/*.py           -> passed
test -s docs/assets/interactive/inference-flow.html -> passed
mkdocs build --strict                        -> passed
```

## Remaining external step

GitHub Pages must be enabled at **Settings → Pages → Source: GitHub Actions**. The standard workflow token cannot enable Pages for the repository. After enablement, rerun `Deploy documentation`; its final job verifies the live page.
