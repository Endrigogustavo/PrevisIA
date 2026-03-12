from __future__ import annotations

import statistics
from dataclasses import dataclass
from datetime import timedelta

from .storage import TemperatureRecord


@dataclass(frozen=True)
class Recommendation:
    next_day: str
    predicted_temperature: float
    confidence: str
    summary: str


def _weighted_moving_average(values: list[float]) -> float:
    weights = list(range(1, len(values) + 1))
    weighted_sum = sum(value * weight for value, weight in zip(values, weights))
    return weighted_sum / sum(weights)


def _trend_slope(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0

    x_values = list(range(len(values)))
    x_mean = statistics.fmean(x_values)
    y_mean = statistics.fmean(values)

    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, values))
    denominator = sum((x - x_mean) ** 2 for x in x_values)

    if denominator == 0:
        return 0.0
    return numerator / denominator


def _build_summary(predicted_temperature: float, volatility: float) -> str:
    if predicted_temperature >= 32:
        base = "Calor forte previsto; hidrate-se e evite exposicao longa ao sol."
    elif predicted_temperature >= 26:
        base = "Dia quente previsto; prefira roupas leves e mantenha hidratacao."
    elif predicted_temperature >= 20:
        base = "Temperatura amena prevista; dia confortavel para atividades externas."
    elif predicted_temperature >= 14:
        base = "Clima fresco previsto; leve um agasalho leve."
    else:
        base = "Frio previsto; use roupas mais quentes e proteja-se do vento."

    if volatility >= 5:
        return f"{base} O historico recente mostra alta variacao termica."
    return base


def generate_recommendation(records: list[TemperatureRecord]) -> Recommendation:
    if not records:
        return Recommendation(
            next_day="sem dados",
            predicted_temperature=25.0,
            confidence="baixa",
            summary="Ainda nao ha historico. Registre alguns dias para melhorar a previsao.",
        )

    temperatures = [rec.temperature for rec in records]
    recent = temperatures[-7:]
    moving_average = _weighted_moving_average(recent)
    trend = _trend_slope(recent)

    base_prediction = (moving_average * 0.75) + ((temperatures[-1] + trend) * 0.25)
    predicted = max(-10.0, min(45.0, base_prediction))

    if len(recent) > 1:
        volatility = statistics.pstdev(recent)
    else:
        volatility = 0.0

    if len(records) >= 10 and volatility <= 3:
        confidence = "alta"
    elif len(records) >= 5:
        confidence = "media"
    else:
        confidence = "baixa"

    summary = _build_summary(predicted, volatility)
    next_day = (records[-1].day + timedelta(days=1)).isoformat()

    return Recommendation(
        next_day=next_day,
        predicted_temperature=round(predicted, 1),
        confidence=confidence,
        summary=summary,
    )
