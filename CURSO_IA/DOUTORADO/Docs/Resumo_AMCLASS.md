## Resumo de Estudo: Métodos Clássicos de Aprendizagem de Máquina

# 1. Introdução à Biblioteca Scikit-Learn
A biblioteca Scikit-Learn foi concebida em 2007 por David Cournapeau no âmbito do projeto Google Summer of Code. Como docente e engenheiro, é fundamental destacar que esta ferramenta de código aberto para Python é o pilar para o trabalho com a  matriz experimental . Ela integra-se de forma simbiótica com o ecossistema científico de bibliotecas como  Seaborn, Matplotlib, NumPy e Pandas , sendo essencial para a implementação de modelos estatísticos e de Aprendizado de Máquina (Machine Learning).Vantagens e Desvantagens:
Vantagens:
Facilidade de uso:  Interface intuitiva que permite rápida prototipagem e experimentação.
Padronização:  Estrutura consistente que simplifica o fluxo de construção e implementação de modelos variados.
Desvantagens:
Baixa flexibilidade:  A abstração de alto nível limita o ajuste fino granular de parâmetros ou o design de arquiteturas customizadas complexas.
Aprendizagem Profunda:  Não é a plataforma recomendada para quem foca especificamente em redes neurais complexas ou  Deep Learning .

# 2. Fluxo de Trabalho e Seleção de Algoritmos
A escolha do modelo não deve ser arbitrária. O conceito de  "namorar os dados"  é a base da Engenharia de Dados bem-sucedida, exigindo um rigoroso processo de compreensão antes da codificação.
Compreensão e Filtragem dos Dados:  É o primeiro passo para filtrar algoritmos incapazes de processar o conjunto disponível. Deve-se observar o volume de instâncias, a qualidade e significância das medidas e, crucialmente, se as características são  dependentes ou independentes entre si .
Categorização do Problema:  Identifica-se se os dados são estruturados (tabelas) ou não estruturados (imagens/texto). Define-se o regime de aprendizado:
Supervisionado:  Dados possuem rótulos (saídas desejadas).
Semi-supervisionado:  Quando apenas uma  parte menor dos dados possui rótulo .
Não supervisionado:  Ausência total de rótulos.
Seleção do Conjunto de Algoritmos:  Esta etapa é o  "ponto de virada"  que diferencia modelos de excelência de resultados medíocres. A boa prática docente exige a avaliação de múltiplos algoritmos de uma mesma "família" para determinar o desempenho superior na aplicação específica.

# 3. Engenharia de Características: Pré-processamento e Redimensionamento
O redimensionamento é imperativo para garantir que o modelo não priorize variáveis apenas pela magnitude numérica de sua escala, ignorando seu peso semântico."A normalização permite que o modelo atribua os mesmos pesos a todos os dados, possibilitando a generalização correta. Sem isso, o algoritmo teria dificuldades em processar, simultaneamente, variáveis com escalas discrepantes, como a  Umidade Relativa %  do dia a dia comparada à  temperatura do sol ou de um forno industrial ."Técnicas de Redimensionamento:
Normalização (Min-Max Scaling):  Redimensiona os dados para o intervalo estrito entre 0 e 1.
Fórmula:  $z_i = \frac{x_i - \min(x)}{\max(x) - \min(x)}$
Padronização (Standardization):  Transforma os dados em uma Distribuição Gaussiana com média 0 e desvio padrão 1.
Fórmula:  $z_i = \frac{x_i - \text{media}(x)}{\text{std}(x)}$Nota Técnica: Embora muitos pesquisadores utilizem o termo "normalização" genericamente para ambos os métodos, o engenheiro deve selecionar a metodologia mais aceita na sua respectiva área de interesse.

# 4. Modelos de Regressão e Casos Práticos
Os modelos de regressão buscam modelar a relação entre variáveis para prever valores contínuos.| Tipo de Regressão | Conceito Chave | Exemplo Prático (Fonte) || ------ | ------ | ------ || Regressão Linear | Relação linear entre variáveis dependentes e independentes. | Estudo de Galton (alturas); Progressão de  Diabetes  (10 variáveis independentes e  6 medidas de soro sanguíneo  em 442 pacientes). || Regressão Polinomial | Adaptação a relações não lineares usando polinômios de grau  n . | Ajuste de curvas onde a tendência dos dados não segue uma linha reta. || Análise de Correlação | Avalia a força da relação para tratar variáveis preditoras. | Prevenção de  multicolinearidade  no conjunto de dados. |

# 5. Aprendizado por Conjuntos (Ensembles) e Metaclassificação
A teoria de Ensembles fundamenta-se na premissa de que a combinação de modelos supera o desempenho individual. Como ensina o ditado chinês:  "Três sapateiros com sua inteligência combinada podem superar Zhūgě Liàng, o mestre" . Este é o cerne do "Bom Trabalho" colaborativo em IA.A  Votação Majoritária  pode ser decidida por:
Unanimidade:  Consenso total dos modelos.
Maioria:  Acima de 50% de concordância.
Pluralidade:  O rótulo com maior número de votos, independente de maioria absoluta.Conceito de Boosting e XGBoost:  O Boosting foca em uma sequência de modelos onde cada um corrige os erros do anterior. O algoritmo  XGBoost  deve ser comparado a modelos de base como Árvore de Decisão e Floresta Aleatória para validação de ganho. Para eficiência, utiliza-se o  Critério de Parada Precoce (Early Stopping) , interrompendo o treino quando o ganho de desempenho deixa de ser estatisticamente significativo.

# 6. Interpretabilidade e Ajuste de Modelos
Ferramentas para garantir que o modelo não seja apenas performático, mas também transparente (explicável).
Hiperparâmetros:  Variáveis de configuração externas ao aprendizado direto do modelo, ajustadas manualmente pelo engenheiro para otimização fina.
Pipeline:  Ferramenta que facilita a  automação  de etapas de pré-processamento e treinamento, mitigando erros manuais no fluxo de trabalho.
SHAP (SHapley Additive exPlanations):  Baseado em teoria dos jogos, fornece visibilidade ao funcionamento de modelos  "caixa-preta" . Através de sua  propriedade aditiva , permite calcular a importância das características e recuperar probabilidades previstas.

# 7. Matriz de Exercícios e Aplicações Reais
Lista de verificação para consolidação do aprendizado laboratorial:
  Titanic:  Análise da probabilidade de sobrevivência em função dos diferentes conveses ocupados.
  Diabetes:  Predição da  progressão da doença após um ano , correlacionando variáveis sanguíneas e índices corporais.
  Galton:  Aplicação histórica de predição de altura (introdução ao conceito de regressão).
  Publicidade:  Modelo regressor para prever vendas com base em investimentos em TV, Rádio e Jornal.
  Escore de Crédito:  Análise do arquivo EscoreCredito.csv com comparação de performance entre  XGBoost, Árvore de Decisão e Floresta Aleatória .
