"""Transparent compensation-calculation demo.

The formula and multiplier are illustrative. Confirm the applicable law,
state rules, valuation basis and any additional components before real use.
"""
from statistics import mean, pstdev


def calculate_award(market_value: float, multiplier: float,
                    assets: float = 0.0, solatium_rate: float = 1.0) -> dict:
    """Return a readable breakdown instead of one unexplained total."""
    if market_value < 0 or assets < 0:
        raise ValueError("Market value and assets cannot be negative.")
    if multiplier <= 0:
        raise ValueError("Multiplier must be greater than zero.")
    if not 0 <= solatium_rate <= 1:
        raise ValueError("Solatium rate must be between 0 and 1.")

    land_value = market_value * multiplier
    solatium = (land_value + assets) * solatium_rate
    total = land_value + assets + solatium

    return {
        "land_value": round(land_value, 2),
        "assets": round(assets, 2),
        "solatium": round(solatium, 2),
        "total": round(total, 2),
    }


def anomaly_z_score(value: float, comparable_values: list[float]) -> float:
    """Simple outlier signal for demo use; not proof of wrongdoing."""
    if len(comparable_values) < 2:
        raise ValueError("At least two comparable values are required.")
    sd = pstdev(comparable_values)
    if sd == 0:
        return 0.0
    return (value - mean(comparable_values)) / sd


if __name__ == "__main__":
    award = calculate_award(
        market_value=1_200_000,
        multiplier=1.5,
        assets=150_000,
        solatium_rate=1.0,
    )
    print(f"Land value : Rs {award['land_value']:,.0f}")
    print(f"Assets     : Rs {award['assets']:,.0f}")
    print(f"Solatium   : Rs {award['solatium']:,.0f}")
    print(f"TOTAL AWARD: Rs {award['total']:,.0f}")

    comparable = [1_000_000, 1_200_000, 1_100_000, 1_300_000, 1_150_000]
    score = anomaly_z_score(3_900_000, comparable)
    print(f"Anomaly z-score: {score:.2f} "
          f"{'FLAG FOR REVIEW' if abs(score) >= 2 else 'within threshold'}")
