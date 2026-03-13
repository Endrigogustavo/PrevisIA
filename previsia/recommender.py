from __future__ import annotations

import statistics
from dataclasses import dataclass
from datetime import timedelta
import math

from .storage import TemperatureRecord


@dataclass(frozen=True)
class Recommendation:
    next_day: str
    predicted_temperature: float
    predicted_humidity: float | None
    confidence: str
    summary: str
    apparent_temperature: float | None


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


def _apparent_temperature(temp: float, humidity: float) -> float:
    """Sensacao termica usando formula de Steadman simplificada (Celsius, %)."""
    e = (humidity / 100) * 6.105 * math.exp(17.27 * temp / (237.7 + temp))
    return temp + 0.348 * e - 4.25


def _build_summary(predicted_temperature: float, volatility: float, humidity: float | None) -> str:
    if predicted_temperature >= 32:
        if humidity is not None and humidity >= 70:
            base = "Calor forte e abafado previsto; o ar umido dificulta a transpiracao. Hidrate-se bastante."
        elif humidity is not None and humidity < 35:
            base = "Calor forte e seco previsto; use protetor solar e beba muita agua."
        else:
            base = "Calor forte previsto; hidrate-se e evite exposicao longa ao sol."
    elif predicted_temperature >= 26:
        if humidity is not None and humidity >= 70:
            base = "Dia quente e umido previsto; prefira ambientes ventilados e roupas leves."
        elif humidity is not None and humidity < 35:
            base = "Dia quente e seco previsto; umidifique ambientes e mantenha hidratacao."
        else:
            base = "Dia quente previsto; prefira roupas leves e mantenha hidratacao."
    elif predicted_temperature >= 20:
        base = "Temperatura amena prevista; dia confortavel para atividades externas."
    elif predicted_temperature >= 14:
        if humidity is not None and humidity >= 80:
            base = "Clima fresco e umido previsto; leve agasalho e prefira roupas impermeabilizadas."
        else:
            base = "Clima fresco previsto; leve um agasalho leve."
    else:
        if humidity is not None and humidity >= 75:
            base = "Frio e umido previsto; use roupas quentes e impermeavel."
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
            predicted_humidity=None,
            confidence="baixa",
            summary="Ainda nao ha historico. Registre alguns dias para melhorar a previsao.",
            apparent_temperature=None,
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

    # Previsao de umidade
    humidity_values = [rec.humidity for rec in records if rec.humidity is not None]
    if humidity_values:
        recent_humidity = humidity_values[-7:]
        humidity_trend = _trend_slope(recent_humidity)
        predicted_humidity: float | None = max(0.0, min(100.0, round(
            (_weighted_moving_average(recent_humidity) * 0.75) + ((recent_humidity[-1] + humidity_trend) * 0.25), 1
        )))
    else:
        predicted_humidity = None

    apparent = round(_apparent_temperature(predicted, predicted_humidity), 1) if predicted_humidity is not None else None

    if len(records) >= 10 and volatility <= 3:
        confidence = "alta"
    elif len(records) >= 5:
        confidence = "media"
    else:
        confidence = "baixa"

    summary = _build_summary(predicted, volatility, predicted_humidity)
    next_day = (records[-1].day + timedelta(days=1)).isoformat()

    return Recommendation(
        next_day=next_day,
        predicted_temperature=round(predicted, 1),
        predicted_humidity=predicted_humidity,
        confidence=confidence,
        summary=summary,
        apparent_temperature=apparent,
    )
