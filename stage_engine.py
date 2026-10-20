"""Rule-based land-acquisition workflow demo.

This is a prototype example. Have the applicable legal stages, deadlines,
roles and exceptions reviewed before using it for real cases.
"""
from dataclasses import dataclass
from datetime import date
from typing import Dict, Tuple


# stage -> (allowed next stage, illustrative deadline in days, authorised role)
# Deadlines and role mappings below are DEMO CONFIGURATION, not legal advice.
STAGES: Dict[str, Tuple[str, int, str]] = {
    "SIA": ("PRELIM_NOTICE", 180, "LAND_ACQUISITION_OFFICER"),
    "PRELIM_NOTICE": ("OBJECTIONS", 60, "COLLECTOR"),
    "OBJECTIONS": ("DECLARATION", 60, "COLLECTOR"),
    "DECLARATION": ("AWARD", 365, "COLLECTOR"),
    "AWARD": ("PAYMENT", 30, "FINANCE_OFFICER"),
    "PAYMENT": ("POSSESSION", 90, "LAND_ACQUISITION_OFFICER"),
    "POSSESSION": ("MUTATION", 30, "REVENUE_OFFICER"),
    "MUTATION": ("COMPLETE", 0, "REVENUE_OFFICER"),
    "COMPLETE": ("COMPLETE", 0, "ADMIN"),
}


class IllegalTransition(ValueError):
    """Raised when a parcel is moved to an unapproved stage."""


class PermissionDenied(PermissionError):
    """Raised when the actor is not allowed to approve a transition."""


class OpenObjectionError(ValueError):
    """Raised when an unresolved objection blocks progression."""


@dataclass
class Parcel:
    khasra: str
    stage: str
    entered_on: date
    open_objections: int = 0


def advance(parcel: Parcel, target: str, role: str, today: date) -> Parcel:
    """Validate and apply one workflow transition."""
    if parcel.stage not in STAGES:
        raise IllegalTransition(f"Unknown current stage: {parcel.stage}")

    expected_target, _deadline, expected_role = STAGES[parcel.stage]

    if target != expected_target:
        raise IllegalTransition(
            f"{parcel.stage} -> {target} is not allowed; expected {expected_target}"
        )

    if role != expected_role and role != "ADMIN":
        raise PermissionDenied(
            f"Role {role} cannot approve {parcel.stage} -> {target}; "
            f"required role: {expected_role}"
        )

    if parcel.open_objections > 0 and parcel.stage == "OBJECTIONS":
        raise OpenObjectionError(
            f"{parcel.open_objections} open objection(s) block progression"
        )

    parcel.stage = target
    parcel.entered_on = today
    return parcel


def sla_breached(parcel: Parcel, today: date) -> bool:
    """Return True when the configured illustrative stage deadline is exceeded."""
    _next_stage, deadline_days, _role = STAGES[parcel.stage]
    return (today - parcel.entered_on).days > deadline_days


if __name__ == "__main__":
    today = date.today()
    parcel = Parcel(khasra="K-102", stage="PRELIM_NOTICE",
                    entered_on=today, open_objections=0)

    # Invalid jump should be blocked.
    try:
        advance(parcel, "POSSESSION", "COLLECTOR", today)
    except IllegalTransition as exc:
        print(f"BLOCK invalid transition: {exc}")

    # Valid next step should pass.
    advance(parcel, "OBJECTIONS", "COLLECTOR", today)
    print(f"PASS valid transition: current stage = {parcel.stage}")

    # Deadline example: a parcel stuck for 141 days in a 60-day stage.
    old_parcel = Parcel("K-103", "PRELIM_NOTICE",
                        date.fromordinal(today.toordinal() - 141))
    print(f"SLA breached (141 days > 60): {sla_breached(old_parcel, today)}")
