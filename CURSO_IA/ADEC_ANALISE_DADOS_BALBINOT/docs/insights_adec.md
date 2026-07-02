## Diretrizes Científicas para Implementação do Script.

Fundamentos e Metodologias de Preparação de Dados para Modelagem
As principais técnicas para a preparação de dados envolvem procedimentos de Análise Exploratória de Dados (EDA) e Engenharia de Características, dividindo-se nas seguintes frentes de atuação:
1. Técnicas Básicas de Transformação e Organização (EDA)
Manipulação de Estruturas: Agrupamento, anexação (fusão), concatenação e mesclagem (merge) de dados.
Limpeza Básica: Ordenação, categorização, remoção de dados duplicados e alteração do formato original dos dados.
2. Tratamento de Problemas Comuns nos Dados
Dados Ausentes: O tratamento pode ser feito pela exclusão (remoção da amostra ou da coluna inteira) ou pela imputação, que é a substituição dos valores faltantes usando métricas estatísticas (média, mediana), preenchimento sequencial (baseado no último valor) ou uso de modelos inteligentes, como o vizinhos mais próximos (k-NN) e a regressão.
Ruídos e Outliers (Valores Atípicos): A identificação de valores discrepantes é feita por métodos estatísticos univariados (escore z, boxplot/IQR), bivariados (gráficos de dispersão) ou multivariados (distância Mahalanobis, algoritmos como DBSCAN, LOF e Floresta Isolada). Após a detecção, os outliers podem ser excluídos (procedimento de corte), ter um valor limite determinado ou ser substituídos/interpolados de forma cuidadosa para não introduzir viés.
Desbalanceamento de Classes: Para bases onde uma classe é muito maior que outra, aplicam-se técnicas de reamostragem, como a subamostragem (redução da classe majoritária) e a sobreamostragem (geração sintética de dados para a classe minoritária). Os algoritmos mais famosos para criação sintética de dados são o SMOTE e o ADASYN.
3. Metodologias de Engenharia de Características (Feature Engineering)
Melhoria de Características: Transformações matemáticas aplicadas aos dados para aumentar sua previsibilidade. O principal exemplo é o redimensionamento (ou reescalonamento), que engloba a normalização (colocar todos os valores entre 0 e 1) e a padronização (transformar os dados em uma distribuição Gaussiana com média 0 e desvio padrão 1).
Seleção de Características: Eliminação de variáveis pouco úteis ou repetitivas para encontrar o melhor subconjunto de dados, visando reduzir a dependência entre variáveis e tornar o modelo mais rápido e eficiente.
Construção de Características: Criação de novos atributos relevantes a partir das características existentes, muitas vezes usando operações como multiplicação ou divisão.
Extração de Características e Redução de Dimensionalidade: Transformações matemáticas em um conjunto de variáveis para criar um novo conjunto muito menor, combatendo lentidão e ruído computacional. O método linear mais notório é o PCA (Análise do Componente Principal), acompanhado de opções como o SVD, t-SNE e UMAP.
Aprendizado de Características: Uso de métodos de inteligência artificial (como Autoencoders, Redes Adversariais Generativas e Máquinas de Boltzmann) para aprender representações vetorizadas e criar recursos estruturados automaticamente a partir de fontes não estruturadas.