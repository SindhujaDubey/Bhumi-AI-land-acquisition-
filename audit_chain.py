"""Tamper-evident hash-chain audit-log demo."""
import hashlib
import json
from datetime import datetime, timezone


def digest(row: dict) -> str:
    """Hash a row's content, excluding its own hash field."""
    payload = {key: value for key, value in row.items() if key != "hash"}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def add_event(log: list[dict], actor: str, action: str,
              before: str, after: str) -> dict:
    previous_hash = log[-1]["hash"] if log else "0" * 64
    row = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actor": actor,
        "action": action,
        "before": before,
        "after": after,
        "prev_hash": previous_hash,
    }
    row["hash"] = digest(row)
    log.append(row)
    return row


def verify(log: list[dict]) -> tuple[bool, str | None]:
    """Check row hashes and links to previous rows."""
    previous_hash = "0" * 64
    for index, row in enumerate(log):
        if row.get("prev_hash") != previous_hash:
            return False, f"previous-hash mismatch at row {index}"
        if row.get("hash") != digest(row):
            return False, f"content hash mismatch at row {index}"
        previous_hash = row["hash"]
    return True, None


if __name__ == "__main__":
    audit_log = []
    add_event(audit_log, "collector", "STAGE_CHANGE",
              "OBJECTIONS", "DECLARATION")
    add_event(audit_log, "finance_officer", "PAYMENT_STATUS",
              "pending", "credited")

    print("verify (untouched):", verify(audit_log))

    # Simulate tampering for the demo.
    audit_log[0]["after"] = "AWARD"
    print("verify (row 0 edited):", verify(audit_log))
