# LAB02B — Regressão Logística com `diabetesgravidez.csv`

Atue como um Cientista de Dados e Engenheiro de Machine Learning, com foco didático em Python e `scikit-learn`.

Estou realizando a tarefa do laboratório **LAB02B**, relacionada à aplicação de **Regressão Logística** para classificação supervisionada usando a base de dados:

```text
diabetesgravidez.csv
```

A variável-alvo é:

```text
label
```

As variáveis de entrada esperadas são:

```text
pregnant, insulin, bmi, age, glucose, bp, pedigree
```

## Regras importantes antes de começar

1. Inspecione apenas os arquivos necessários para a tarefa, priorizando:

   * `diabetesgravidez.csv`;
   * o notebook, código ou instruções referentes ao LAB02B.

2. Não leia arquivos grandes ou pastas inteiras sem necessidade.

3. Não imprima a base de dados completa no terminal, notebook ou resposta.

4. Para conhecer a estrutura da base, mostre inicialmente somente:

```python
df.head()
df.shape
df.info()
df.describe()
```

5. Use a base completa apenas para:

   * EDA;
   * tratamento de dados;
   * treinamento;
   * teste;
   * cálculo das métricas;
   * geração dos gráficos.

6. Não invente resultados numéricos, métricas ou conclusões. Execute o código localmente quando possível e utilize apenas os resultados reais obtidos.

7. Não altere o arquivo original `diabetesgravidez.csv`. Caso seja necessário modificar dados, trabalhe sobre uma cópia do DataFrame.

8. Escreva comentários didáticos em português, explicando o objetivo de cada bloco de código.

# Objetivo da tarefa
Expandir a aplicação de Regressão Logística da base `diabetesgravidez.csv`, avaliando o efeito de:
1. ajuste do número de iterações do algoritmo;
2. tratamento de dados ausentes ou valores clinicamente inválidos;
3. identificação e tratamento de valores anômalos;
4. normalização ou padronização das variáveis;
5. comparação do desempenho do modelo antes e depois dessas intervenções.

# 1. Carregamento e inspeção inicial dos dados

Execute as seguintes etapas:
* importar bibliotecas necessárias;
* carregar o arquivo `diabetesgravidez.csv`;
* mostrar as cinco primeiras linhas;
* mostrar dimensão da base;
* mostrar tipos de dados;
* mostrar estatísticas descritivas;
* verificar distribuição da variável-alvo `label`.

Utilize bibliotecas como:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```

Crie uma seção markdown:

```markdown
# 2. Análise Exploratória de Dados (EDA)
```

Realize uma análise focada em:

## 2.1 Dados ausentes
Verifique valores ausentes tradicionais usando:

```python
df.isnull().sum()
```

Além disso, investigue valores iguais a zero em variáveis clínicas nas quais zero pode representar dado ausente ou valor fisiologicamente improvável, especialmente:

```text
glucose, bp, insulin, bmi
```

Explique que, dependendo da base, valores iguais a zero nessas colunas podem não representar uma medição clínica válida.

Mostre uma tabela com a quantidade de zeros por coluna relevante.

## 2.2 Distribuições e possíveis outliers

Gere gráficos adequados, sem exagerar na quantidade:

* histogramas ou gráficos de densidade das principais variáveis;
* boxplots para identificação visual de valores anômalos;
* mapa de correlação entre as variáveis numéricas e `label`.

Priorize as colunas:

```text
pregnant, glucose, bp, insulin, bmi, pedigree, age
```

## 2.3 Estratégia para tratamento

Com base na EDA, proponha e implemente uma estratégia justificada para tratar:

* valores ausentes;
* valores zero clinicamente inválidos;
* possíveis outliers.

Sugestões aceitáveis:

* substituir zeros inválidos por `NaN`;
* imputar valores ausentes pela mediana;
* avaliar outliers pelo método do intervalo interquartil, IQR;
* limitar valores extremos por winsorização ou manter os dados caso os valores sejam clinicamente plausíveis.

Explique claramente qual método foi adotado e por quê.

Não remova observações automaticamente sem justificar o impacto dessa decisão.


# 3. Separação entre treino e teste

Crie uma seção:

```markdown
# 3. Separação dos dados em treino e teste
```

Separe as variáveis de entrada e a variável-alvo:

```python
X = df[features]
y = df["label"]
```

Utilize divisão treino/teste de 70/30, com estratificação da variável-alvo:

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)
```

Explique por que `stratify=y` é importante em um problema de classificação.

---

# 4. Modelo base e ajuste de iterações

Crie uma seção:

```markdown
# 4. Regressão Logística — modelo base e número de iterações
```

Treine uma Regressão Logística inicial usando os dados brutos.

Utilize, por exemplo:

```python
from sklearn.linear_model import LogisticRegression

modelo_base = LogisticRegression(
    max_iter=1000,
    random_state=42
)
```

Explique:

* o que é o parâmetro `max_iter`;
* por que ele pode precisar ser aumentado;
* a relação entre falta de convergência e mensagens como `ConvergenceWarning`;
* como a normalização pode facilitar a convergência do modelo.

Teste e compare pelo menos dois valores de `max_iter`, por exemplo:

```text
100 e 1000
```

Registre se houve aviso de convergência e qual valor foi adotado no restante da análise.

---

# 5. Cenários de comparação

Crie uma seção:

```markdown
# 5. Comparação entre cenários
```

Avalie obrigatoriamente os três cenários abaixo.

## Cenário A — Dados brutos

Treine o modelo usando os dados originais, realizando apenas o ajuste necessário em `max_iter`.

Não aplique imputação, remoção de outliers ou normalização nesse cenário.

## Cenário B — Dados tratados

Treine o modelo após:

* identificar e tratar zeros clinicamente inválidos;
* imputar dados ausentes;
* aplicar a estratégia definida para valores anômalos.

Não aplique normalização nesse cenário.

## Cenário C — Dados tratados e normalizados

Treine o modelo após o mesmo tratamento do Cenário B e aplique padronização das variáveis.

Utilize preferencialmente:

```python
from sklearn.preprocessing import StandardScaler
```

Aplique o scaler corretamente:

```python
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

Explique por que o `fit()` deve ocorrer apenas no conjunto de treino, evitando vazamento de dados.

---

# 6. Pipelines

Sempre que possível, utilize `Pipeline` do `scikit-learn` para evitar vazamento de dados e organizar o fluxo de pré-processamento.

Exemplo conceitual:

```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
```

Para o Cenário C, use uma pipeline com:

1. imputação;
2. normalização;
3. regressão logística.

Para o Cenário B, use uma pipeline com:
1. zeros_invalidos;
2. imputação;
3. winsorização;
4. regressão logística.

Explique brevemente a vantagem de usar pipelines.

---

# 7. Métricas de avaliação

Crie uma seção:

```markdown
# 7. Avaliação dos modelos
```

Avalie cada cenário usando:

* Acurácia;
* Precisão;
* Recall;
* F1-score;
* Matriz de confusão;
* Relatório de classificação.

Utilize recursos como:

```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay
)
```

Gere uma tabela final comparando os três cenários com as métricas:

```text
Cenário | Acurácia | Precisão | Recall | F1-score
```

Mostre também uma matriz de confusão para cada cenário.

---

# 8. Interpretação dos resultados

Crie uma seção Markdown chamada:

```markdown
# 8. Interpretação dos resultados
```

Interprete os resultados reais obtidos, abordando:

1. se o aumento de `max_iter` foi necessário;
2. se havia valores zero ou ausentes relevantes;
3. se o tratamento de dados alterou as métricas;
4. se a normalização melhorou a convergência ou o desempenho;
5. qual cenário apresentou o melhor equilíbrio entre precisão, recall e F1-score;
6. limitações da análise, principalmente relacionadas ao tamanho e à qualidade da base.

Evite conclusões genéricas. Baseie a interpretação nos valores reais calculados pelo notebook.

---

# 9. Relatório técnico final

Após executar o notebook, produza um relatório técnico em Markdown com a estrutura:

```markdown
# Relatório Técnico — Regressão Logística na Base diabetesgravidez.csv

## 1. Introdução

## 2. Metodologia

## 3. Análise Exploratória de Dados

## 4. Tratamento dos Dados

## 5. Modelagem e Ajuste de Iterações

## 6. Resultados e Comparação dos Cenários

## 7. Conclusão
```

O relatório deve:

* estar em português;
* ser objetivo e adequado para entrega acadêmica;
* citar os resultados reais do notebook;
* explicar o efeito do tratamento e da normalização;
* não conter valores inventados;
* não repetir blocos extensos de código.

---

# Entregáveis esperados

Crie ou atualize os seguintes arquivos:

```text
1. tarefa_lab02_diabetes.ipynb
2. relatorio_lab02_diabetes.md
```

O notebook deve conter:

* células Markdown explicativas;
* células de código bem comentadas;
* gráficos;
* tabela comparativa;
* métricas;
* conclusões finais.

O relatório em Markdown deve conter apenas a síntese técnica e os resultados da execução.

Ao terminar, informe:

1. quais arquivos foram criados ou alterados;
2. se o código foi executado sem erros;
3. se houve avisos de convergência;
4. qual cenário apresentou o melhor desempenho.
