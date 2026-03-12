# PrevisIA

PrevisIA e um projeto Python que registra temperaturas diarias e gera uma recomendacao inteligente para o dia seguinte, simulando um comportamento de IA a partir do historico.

## Como funciona

- Voce registra a temperatura de cada dia.
- O sistema salva os dados em um arquivo CSV local.
- A previsao usa media movel ponderada + tendencia recente.
- A cada novo registro, a recomendacao para o proximo dia e recalculada.

## Requisitos

- Python 3.10+

## Instalacao

1. (Opcional) Crie e ative um ambiente virtual.
2. Instale dependencias:

	python -m pip install -r requirements.txt

## Uso

Registrar temperatura de um dia:

python app.py add --day 2026-03-10 --temp 28.4 --city curitiba

Gerar recomendacao para o proximo dia com base no historico:

python app.py recommend

Mostrar historico salvo:

python app.py history

## Estrutura

- app.py: interface de linha de comando.
- previsia/storage.py: leitura e escrita do historico.
- previsia/recommender.py: logica de previsao e recomendacao.
- data/temperatures.csv: base local criada automaticamente.

## Observacoes

- Se registrar novamente a mesma data, o valor antigo e substituido.
- Quanto maior o historico, melhor tende a ficar a recomendacao.