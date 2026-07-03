# Relatório Técnico — Regressão Logística na Base diabetesgravidez.csv

## 1. Introdução

Este relatório documenta a aplicação de Regressão Logística à base `diabetesgravidez.csv`, com o objetivo de classificar a variável-alvo `label` a partir das variáveis `pregnant`, `insulin`, `bmi`, `age`, `glucose`, `bp` e `pedigree`. O trabalho foi conduzido no notebook `tarefa_lab02_diabetes.ipynb`, e os resultados aqui apresentados correspondem exatamente às métricas obtidas em sua execução.

## 2. Metodologia

A base contém 768 registros e 9 colunas. A variável-alvo `label` está distribuída em 500 casos negativos (65,1%) e 268 casos positivos (34,9%), configurando um desbalanceamento moderado. Os dados foram divididos em treino e teste na proporção 70/30 (537 registros de treino e 231 de teste), com `random_state=42` e estratificação pela variável-alvo, o que preservou a proporção de classes em ambos os conjuntos (treino: 350 classe 0 e 187 classe 1; teste: 150 classe 0 e 81 classe 1). Foram comparados três cenários — dados brutos, dados tratados e dados tratados com padronização —, todos avaliados sobre a mesma partição de teste.

## 3. Análise Exploratória de Dados (EDA)

Não foram encontrados valores ausentes tradicionais (`NaN`) em nenhuma coluna. Entretanto, a inspeção de zeros clinicamente inválidos revelou: 5 zeros em `glucose`, 35 em `bp`, 374 em `insulin` e 11 em `bmi` — o caso de `insulin` é particularmente relevante, pois quase metade dos registros (48,7%) apresenta valor zero, o que é fisiologicamente improvável e sugere ausência de medição. Histogramas, boxplots e o mapa de correlação confirmaram a presença de assimetrias e valores extremos nas variáveis `insulin`, `bp`, `bmi` e `pedigree`, reforçando a necessidade de tratamento antes da modelagem.

## 4. Tratamento dos Dados

A estratégia adotada seguiu quatro etapas, aplicadas por meio de `Pipeline` do scikit-learn para evitar vazamento de dados: (1) substituição dos zeros inválidos por `NaN` em `glucose`, `bp`, `insulin` e `bmi`; (2) imputação dos valores ausentes pela mediana; (3) limitação de valores extremos por winsorização, com limites definidos pelo critério do intervalo interquartil (IQR, fator 1,5); (4) padronização via `StandardScaler`, aplicada apenas no Cenário C. Em todos os casos, os parâmetros de imputação, winsorização e padronização foram ajustados exclusivamente no conjunto de treino e apenas aplicados (`transform`) ao conjunto de teste.

## 5. Modelagem e Ajuste de max_iter

O parâmetro `max_iter` define o número máximo de iterações do otimizador da Regressão Logística. Foram comparados os valores 100 e 1000 sobre os dados brutos de treino: com `max_iter=100`, o modelo convergiu utilizando apenas 95 iterações, sem gerar `ConvergenceWarning`; o mesmo ocorreu com `max_iter=1000`. Ou seja, o aumento do limite não foi necessário nesta execução. Ainda assim, `max_iter=1000` foi adotado nos três cenários comparativos, por segurança e para manter a comparação padronizada entre eles.

## 6. Resultados

A tabela a seguir apresenta as métricas reais obtidas para a classe positiva (`label=1`) em cada cenário:

| Cenário | Acurácia | Precisão | Recall | F1-score |
|---|---:|---:|---:|---:|
| A - Dados brutos | 0,7403 | 0,6667 | 0,5185 | 0,5833 |
| B - Dados tratados | 0,7403 | 0,6567 | 0,5432 | 0,5946 |
| C - Dados tratados e padronizados | 0,7403 | 0,6567 | 0,5432 | 0,5946 |

As matrizes de confusão (linhas = classe real, colunas = classe prevista, ordem [0, 1]) foram:

- Cenário A: `[[129, 21], [39, 42]]`
- Cenário B: `[[127, 23], [37, 44]]`
- Cenário C: `[[127, 23], [37, 44]]`

O tratamento dos dados (Cenário B) manteve a acurácia em 0,7403, mas aumentou o recall de 0,5185 para 0,5432 e o F1-score de 0,5833 para 0,5946, ao custo de uma pequena queda de precisão (de 0,6667 para 0,6567) — ou seja, o modelo passou a identificar mais casos positivos reais, com uma proporção levemente maior de falsos positivos. A padronização (Cenário C) não alterou nenhuma métrica em relação ao Cenário B nesta divisão treino/teste, tampouco foi necessária para evitar avisos de convergência, já que nenhum cenário os apresentou.

## 7. Conclusão

Os resultados reais indicam que o tratamento de zeros clinicamente inválidos, a imputação pela mediana e a winsorização por IQR melhoraram a capacidade do modelo de identificar corretamente pacientes positivos (recall e F1-score), sem alterar a acurácia geral. A padronização das variáveis, embora recomendada como boa prática para modelos sensíveis à escala, não produziu ganho numérico adicional nesta execução. Considerando o equilíbrio entre precisão, recall e F1-score, os Cenários B e C empataram como melhores, com F1-score de 0,5946. A análise é limitada pelo tamanho moderado da base, pela alta proporção de zeros inválidos em `insulin` (48,7%) e pelo uso de uma única divisão treino/teste; validação cruzada poderia fornecer uma estimativa mais estável de desempenho.
