# PredictKit 🔧

> **Python + C IoT SDK — reduce 300 lines of boilerplate to 5**

[![PyPI version](https://img.shields.io/pypi/v/predictkit)](https://pypi.org/project/predictkit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![CI](https://github.com/sharanabasaveshwar/predictkit/actions/workflows/ci.yml/badge.svg)](https://github.com/sharanabasaveshwar/predictkit/actions/workflows/ci.yml)

---

## The Problem

Every IoT developer spends 60–70% of project time writing the same boilerplate:
MQTT reconnection logic, sensor data normalisation, anomaly detection pipelines,
alert routing. Over and over, project after project.

## The Solution

```python
from predictkit import SensorStream, AnomalyDetector

stream   = SensorStream(source="mqtt://factory.local", topics=["temp", "vibration"])
detector = AnomalyDetector(model="zscore", threshold=80)
stream.on_anomaly(detector, alert="email:admin@company.com")
stream.start()   # Runs forever — auto-reconnect, buffering, error handling included
```

**That replaces ~300 lines of production code.**

---

## Installation

```bash
pip install predictkit            # zero-dependency core
pip install predictkit[mqtt]      # + MQTT support
pip install predictkit[ml]        # + ML anomaly detection
pip install predictkit[all]       # + everything
```

---

## Six Core Modules

| Module | What it replaces | Free tier |
|---|---|---|
| `SensorStream` | MQTT ingestion, auto-reconnect, buffering (~500 lines) | MQTT ✅ |
| `DataNormalizer` | Multi-brand sensor unification (~300 lines) | ✅ |
| `AnomalyDetector` | Plug-and-play ML anomaly detection (~400 lines) | Z-score ✅ |
| `HealthScore` | 0–100 machine health score (~250 lines) | ✅ |
| `AlertRouter` | Multi-channel alerts with retry & rate-limiting (~200 lines) | Email ✅ |
| `EdgeCache` | Offline-first SQLite + cloud sync (~350 lines) | ✅ |

---

## Quick Examples

### Anomaly Detection
```python
from predictkit import AnomalyDetector

detector = AnomalyDetector(model="zscore", threshold=80)
detector.fit(historical_temps)
score = detector.predict(current_temp)   # returns 0–100
```

### Multi-Brand Sensor Normalisation
```python
from predictkit import DataNormalizer

n = DataNormalizer(schema={
    "temperature": {"field": ["temp_C", "TEMP_CEL", "temperature"], "unit": "celsius"},
})
# Works with Siemens, Fanuc, Kirloskar — same output every time
normalized = n.transform(raw_sensor_data)
```

### Machine Health Score
```python
from predictkit import HealthScore

health = HealthScore(sensors={
    "temperature": {"weight": 0.3, "ideal": 70, "max": 90},
    "vibration":   {"weight": 0.5, "ideal": 2.0, "max": 5.0},
})
score = health.calculate({"temperature": 85, "vibration": 4.2})
# → 42  (poor health)
```

---

## Pro Features

| Feature | Free | Pro (₹4,999 one-time) |
|---|---|---|
| MQTT protocol | ✅ | ✅ |
| OPC-UA / Modbus / HTTP | ❌ | ✅ |
| Z-score anomaly detection | ✅ | ✅ |
| Isolation Forest (ML) | ❌ | ✅ |
| LSTM Autoencoder | ❌ | ✅ |
| Email alerts | ✅ | ✅ |
| WhatsApp / SMS / Slack | ❌ | ✅ |
| EdgeCache cloud sync | ✅ | ✅ |
| Priority support (48h SLA) | ❌ | ✅ |

[**→ Get Pro License**](https://predictkit.io/pro)

---

## Contributing

We welcome contributions from the community! Please read the full guide below
before opening a PR.

### Branch strategy

```
master  ──  production only, tagged releases
            ↑
            └── release/x.y.z  (created on release day, PR'd into master)
                                        ↑
dev     ──  active development          └── merged here first, tested, then PR'd to master
            ↑
            └── feature/your-feature   (your daily work branch)
```

**You will never push directly to `dev` or `master`.** Everything goes through a PR.

### Step-by-step contribution flow

**1. Fork & clone**

```bash
git clone https://github.com/sharanabasaveshwar/predictkit.git
cd predictkit
```

**2. Always branch off `dev`**

```bash
git checkout dev
git pull origin dev
git checkout -b feature/your-feature-name
# e.g. feature/add-opcua-driver
#      fix/mqtt-reconnect-timeout
#      docs/update-healthscore-examples
```

**3. Set up your environment**

```bash
pip install -e ".[dev]"
```

**4. Write code + tests**

Every new feature or fix needs a corresponding test in `tests/`.
Run the suite locally before pushing:

```bash
pytest tests/ -v --tb=short
```

**5. Commit with conventional commits**

Every commit message must follow this format:

```
<type>(<optional scope>): <short description in lowercase>
```

| Type | When to use |
|---|---|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, whitespace (no logic change) |
| `refactor` | Code restructure (no feature or fix) |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `build` | Build system, packaging, dependencies |
| `ci` | CI/CD workflow changes |
| `chore` | Maintenance, tooling, config |

Examples:

```bash
git commit -m "feat(stream): add websocket protocol support"
git commit -m "fix(alerts): retry on smtp connection timeout"
git commit -m "docs(readme): add modbus usage example"
git commit -m "refactor(cache): simplify sync thread logic"
git commit -m "test(normalizer): add unit conversion edge cases"
git commit -m "chore: update dev dependencies"
```

Breaking changes use `!` after the type:

```bash
git commit -m "feat(stream)!: rename source param to broker_url"
```

> Merge commits and revert commits are exempt from this rule.
> All other commits are checked automatically by CI when you open a PR.

**6. Push and open a PR to `dev`**

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request targeting the `dev` branch on GitHub.
The PR title should also follow the conventional commit format.

**7. CI checks run automatically**

Your PR must pass all of these before it can be merged:

| Check | What it does |
|---|---|
| `Lint & Format` | `ruff` + `black --check` |
| `Test / ubuntu-latest` | Full pytest suite |
| `Test / macos-latest` | Full pytest suite |
| `Build distribution` | `python -m build` + `twine check` |
| `Lint commit messages` | Conventional commits on every commit |

**8. Request a review**

At least 1 approval is required before merging into `dev`.

---

### Release flow (maintainers only)

On release day:

```bash
# 1. Cut a release branch off dev
git checkout dev && git pull origin dev
git checkout -b release/1.2.0
git push origin release/1.2.0

# 2. Open a PR: release/1.2.0 → master
# 3. CI runs all checks again
# 4. 1 approval required
# 5. On merge → automation kicks in:
#      - Determines version bump from commits (feat→minor, fix→patch, feat!→major)
#      - Updates version in pyproject.toml and __init__.py
#      - Creates git tag  v1.2.0
#      - Creates GitHub Release with auto-generated changelog
```

You never need to manually update version numbers or create tags.

---

### Commit type → version bump mapping

| Commits since last release | Version bump | Example |
|---|---|---|
| Only `fix:`, `chore:`, `docs:` etc | Patch `0.0.x` | `0.1.0` → `0.1.1` |
| At least one `feat:` | Minor `0.x.0` | `0.1.0` → `0.2.0` |
| Any `feat!:` or `BREAKING CHANGE` | Major `x.0.0` | `0.1.0` → `1.0.0` |

---

### What we welcome

- Bug fixes with regression tests
- New protocol drivers (implement the `SensorDriver` interface in `predictkit/drivers/`)
- Improved anomaly detection models (free tier only — no dependencies)
- Documentation and example projects
- Performance improvements with benchmarks

### What we don't accept

- PRs that add heavy dependencies to the zero-dep core
- PRs without tests
- PRs with non-conventional commit messages (CI will block these)

---

## License

MIT — see [LICENSE](LICENSE).
