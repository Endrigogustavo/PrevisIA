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

    subparsers.add_parser("recommend", help="Gera recomendacao para o proximo dia")
    subparsers.add_parser("history", help="Mostra o historico salvo")

    return parser.parse_args()


def _print_history() -> None:
    records = list_temperature_records()
    if not records:
        print("Historico vazio. Use o comando 'add' para registrar temperaturas.")
        return

    print("Historico de temperaturas:")
    for rec in records:
        print(f"- {rec.day.isoformat()}: {rec.temperature:.1f} C")


def _print_recommendation() -> None:
    records = list_temperature_records()
    recommendation = generate_recommendation(records)

    print(f"Proximo dia: {recommendation.next_day}")
    print(f"Temperatura prevista: {recommendation.predicted_temperature:.1f} C")
    print(f"Confianca: {recommendation.confidence}")
    print(f"Recomendacao: {recommendation.summary}")


def _handle_add(day_text: str, temperature: float) -> None:
    try:
        parsed_day = date.fromisoformat(day_text)
    except ValueError as exc:
        raise SystemExit("Data invalida. Use o formato AAAA-MM-DD.") from exc

    add_temperature_record(parsed_day, temperature)
    print(f"Registro salvo: {parsed_day.isoformat()} -> {temperature:.1f} C")
    print("\nNova recomendacao com base no historico atualizado:")
    _print_recommendation()


def main() -> None:
    args = _parse_args()

    if args.command == "add":
        _handle_add(day_text=args.day, temperature=args.temp)
    elif args.command == "history":
        _print_history()
    elif args.command == "recommend":
        _print_recommendation()


if __name__ == "__main__":
    main()
