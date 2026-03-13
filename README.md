# PrevisIA

PrevisIA e um projeto Python que registra temperaturas diarias, umidade do ar e gera uma recomendacao inteligente para o dia seguinte, simulando um comportamento de IA a partir do historico.

## Como funciona

- Voce registra a temperatura de cada dia.
- Opcionalmente, tambem registra a umidade do ar e a cidade.
- O sistema salva os dados em um arquivo CSV local.
- A previsao usa media movel ponderada + tendencia recente.
- Quando ha dados de umidade, o sistema estima a umidade do proximo dia e a sensacao termica.
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

Registrar temperatura com umidade do ar:

python app.py add --day 2026-03-10 --temp 28.4 --humidity 72 --city curitiba

Gerar recomendacao para o proximo dia com base no historico:

python app.py recommend

Gerar recomendacao filtrando por cidade:

python app.py recommend --city curitiba

Mostrar historico salvo:

python app.py history

Mostrar historico de uma cidade, incluindo umidade registrada:

python app.py history --city curitiba

## Estrutura

- app.py: interface de linha de comando.
- previsia/storage.py: leitura e escrita do historico.
- previsia/recommender.py: logica de previsao, umidade e recomendacao.
- data/temperatures.csv: base local criada automaticamente.

## Observacoes

- Se registrar novamente a mesma data para a mesma cidade, o valor antigo e substituido.
- A umidade deve ser informada como percentual entre 0 e 100.
- Quanto maior o historico, melhor tende a ficar a recomendacao.