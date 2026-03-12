from __future__ import annotations

import argparse
from datetime import date

from previsia.recommender import generate_recommendation
from previsia.storage import add_temperature_record, list_temperature_records


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="PrevisIA: recomenda temperatura do dia seguinte com base no historico."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Adiciona ou atualiza um registro diario")
    add_parser.add_argument("--day", required=True, help="Data no formato AAAA-MM-DD")
    add_parser.add_argument(
        "--temp", required=True, type=float, help="Temperatura observada no dia"
    )
    add_parser.add_argument("--city", default="", help="Nome da cidade (opcional)")

    recommend_parser = subparsers.add_parser("recommend", help="Gera recomendacao para o proximo dia")
    recommend_parser.add_argument("--city", default="", help="Nome da cidade (opcional)")

    history_parser = subparsers.add_parser("history", help="Mostra o historico salvo")
    history_parser.add_argument("--city", default="", help="Nome da cidade (opcional)")

    return parser.parse_args()


def _print_history(city: str = "") -> None:
    city_filter = city if city else None
    records = list_temperature_records(city=city_filter)
    if not records:
        city_msg = f" para '{city}'" if city else ""
        print(f"Historico vazio{city_msg}. Use o comando 'add' para registrar temperaturas.")
        return

    city_label = f" ({city})" if city else ""
    print(f"Historico de temperaturas{city_label}:")
    for rec in records:
        city_info = f" [{rec.city}]" if rec.city else ""
        print(f"- {rec.day.isoformat()}: {rec.temperature:.1f} C{city_info}")


def _print_recommendation(city: str = "") -> None:
    city_filter = city if city else None
    records = list_temperature_records(city=city_filter)
    recommendation = generate_recommendation(records)

    if city:
        print(f"Cidade: {city}")
    print(f"Proximo dia: {recommendation.next_day}")
    print(f"Temperatura prevista: {recommendation.predicted_temperature:.1f} C")
    print(f"Confianca: {recommendation.confidence}")
    print(f"Recomendacao: {recommendation.summary}")


def _handle_add(day_text: str, temperature: float, city: str = "") -> None:
    try:
        parsed_day = date.fromisoformat(day_text)
    except ValueError as exc:
        raise SystemExit("Data invalida. Use o formato AAAA-MM-DD.") from exc

    add_temperature_record(parsed_day, temperature, city=city)
    city_info = f" [{city}]" if city else ""
    print(f"Registro salvo: {parsed_day.isoformat()} -> {temperature:.1f} C{city_info}")
    print("\nNova recomendacao com base no historico atualizado:")
    _print_recommendation(city=city)


def main() -> None:
    args = _parse_args()

    if args.command == "add":
        _handle_add(day_text=args.day, temperature=args.temp, city=args.city)
    elif args.command == "history":
        _print_history(city=args.city)
    elif args.command == "recommend":
        _print_recommendation(city=args.city)


if __name__ == "__main__":
    main()
