# BHUMI-AI — Land Acquisition Workflow Demo

A small Python prototype demonstrating three core ideas:
1. Legal-stage workflow validation and deadline flags.
2. Transparent award calculation and a simple compensation outlier signal.
3. Tamper-evident hash-chained audit events.

## Folder structure

```text
land_acquisition_system/
├── stage_engine.py
├── award_calc.py
├── audit_chain.py
├── tests/
│   └── test_stage_engine.py
└── README.md
```

## Run in VS Code

1. Open this folder in VS Code.
2. Ensure Python 3.10+ is installed.
3. Open **Terminal → New Terminal**.
4. Run each demo:

```bash
python stage_engine.py
python award_calc.py
python audit_chain.py
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

No third-party packages are required.

## Important limitations

This is a local proof-of-concept, not a complete production system. Stage transitions, role permissions, deadlines, compensation rules and legal requirements are illustrative configuration and must be reviewed against current applicable law and state rules. The anomaly score is a review signal, not evidence of misconduct. The hash chain detects edits within the recorded chain, but a production system also needs secure storage, access controls, backups and protected signing/anchoring.
