# Contributing to PredictKit

Thanks for your interest! This file is a quick reference.
For the full contribution guide including the branch strategy, commit format,
CI checks, and release process, see the
[Contributing section in the README](README.md#contributing).

---

## Quick start

```bash
git clone https://github.com/sharanabasaveshwar/predictkit.git
cd predictkit
git checkout dev && git pull origin dev
git checkout -b feature/your-feature
pip install -e ".[dev]"
# ... make changes, add tests ...
pytest tests/ -v
git commit -m "feat(scope): short description in lowercase"
git push origin feature/your-feature
# Open PR targeting dev
```

## Conventional commit types

```
feat:      new feature            →  minor version bump
fix:       bug fix                →  patch version bump
feat!:     breaking change        →  major version bump
docs:      documentation
style:     formatting only
refactor:  restructure (no fix/feature)
perf:      performance
test:      tests
build:     packaging / deps
ci:        CI/CD workflows
chore:     maintenance
```

Format: `type(optional-scope): lowercase description`

Merge commits and revert commits are exempt.

## PR checklist

- [ ] Branched from `dev`
- [ ] All tests pass locally (`pytest tests/ -v`)
- [ ] New code has tests
- [ ] All commits follow conventional commit format
- [ ] PR targets `dev`, not `master`
