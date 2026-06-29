## Resumo da ADEC -  Análise Exploratória e Engenharia de Características
# 1. Introdução e Contexto Acadêmico
Este relatório técnico consolida os fundamentos e métricas discutidos no curso de  Especialização em Inteligência Artificial para Engenheiros  da  Universidade Federal do Rio Grande do Sul (UFRGS) , especificamente no âmbito do  Ciclo 2026 . O documento reflete a integração dos conceitos de Análise Exploratória de Dados (AED/EDA) e Engenharia de Características apresentados nas aulas 01B, 01C e 04C, sob a orientação do  Prof. Dr. Alexandre Balbinot . O conteúdo aqui exposto é fruto das atividades desenvolvidas no  Laboratório de Sistemas Eletrônicos Inteligentes (LASEI) , vinculado ao  Departamento de Engenharia Elétrica (DELET) , utilizando ferramentas institucionais como o  Moodle  para aquisição de códigos e o  MCONF  para o acesso aos conjuntos de dados.

# 2. Fundamentos de Análise Exploratória de Dados (AED)
A Análise Exploratória de Dados transcende a mera visualização; ela constitui a etapa de preparação rigorosa necessária para o alinhamento algorítmico. Conforme a "Aula 01B", a AED é o processo de manipulação e interpretação inicial que garante a integridade do pipeline de IA. Este processo sistematiza-se através de nove técnicas essenciais:
Agrupamento de Dados:  Organização de registros por similaridade categórica.
Anexação (Fusão/Append):  Integração vertical de datasets.
Concatenação:  União de dados ao longo de eixos estruturais.
Mesclagem (Merge):  Combinação baseada em chaves relacionais ou colunas comuns.
Ordenação:  Organização baseada em critérios de magnitude ou temporalidade.
Categorização:  Conversão de variáveis contínuas em intervalos discretos ou classes.
Remoção de Duplicatas:  Higienização para evitar o sobreajuste ou viés estatístico.
Alteração do Formato dos Dados:  Ajuste de tipos e estruturas para compatibilidade.
Lidando com Dados Ausentes:  Abordagem inicial de imputação ou descarte crítico.

# 3. Métricas de Tendência Central e Dispersão
A extração de "estatísticas resumidas" é o primeiro passo para o entendimento da distribuição estocástica das variáveis. A aplicação destas métricas permite quantificar a centralidade e a variabilidade dos dados.| Métrica | Aplicação em AED || ------ | ------ || Média | Identificação do centro de gravidade de distribuições simétricas. || Mediana | Representação robusta da tendência central, com alta  robustez a outliers . || Moda | Determinação do valor de maior frequência, vital para dados nominais. || Variância | Mensuração da dispersão quadrática em relação à média. || Desvio Padrão | Escalonamento da dispersão na mesma unidade dos dados originais. || IQR (Amplitude Interquartil) | Quantificação da variabilidade nos 50% centrais; base matemática 
para o  Boxplot |

# 4. Correlação e Interação entre Variáveis
A análise de interdependência entre características (features) é crucial para evitar a redundância e entender a dinâmica do fenômeno modelado:
Pearson:  Coeficiente para detecção de dependências estritamente lineares entre variáveis contínuas.
Spearman:  Métrica baseada em postos que avalia a  monotonocidade  da relação, sendo eficaz para capturar dependências não-lineares e distribuições não-gaussianas.

# 5. Métricas de Distância, Similaridade e Algoritmos Específicos
As métricas de distância fornecem o suporte matemático para a tarefa de  Agrupamento de Dados  (item 1 da seção 2). A escolha da métrica define a topologia do espaço de características:
Distância Euclidiana:  Comprimento do segmento de reta direto entre dois pontos.
Distância de Manhattan:  Soma das diferenças absolutas, ideal para espaços de alta dimensão.
Distância de Mahalanobis:  Abordagem superior para dados com alta correlação, pois incorpora a matriz de covariância na medição da distância entre pontos e a distribuição.
Índice Gini:  Indicador de impureza estatística, fundamental na partição de nós em modelos de árvore.
Silhouette Score (SS):  Validação da consistência dos clusters, comparando a coesão interna com a separação externa.

# 6. Avaliação de Desempenho de Modelos
A eficácia da Engenharia de Características é validada diretamente pelas métricas de desempenho final. Um bom pré-processamento (AED) é o que permite a obtenção de scores elevados em:
Acurácia:  Proporção de predições corretas sobre o total.
Precisão:  Precisão da classe positiva (evita falsos positivos).
Revocação (Recall):  Sensibilidade do modelo (evita falsos negativos).
F1-score:  Equilíbrio harmônico entre precisão e recall, essencial em dados desbalanceados.
AUC ROC:  Medida da capacidade de discriminação entre classes em diferentes limiares.

# 7. Ferramentas de AED Automática e Geração de Insights
A "Aula 04C" introduz bibliotecas que aceleram a geração de insights diagnósticos:
pandas-profiling (YData Profiling):  Especializada na criação de relatórios HTML interativos com matrizes de correlação e alertas automáticos sobre valores ausentes e duplicados.
dtale:  Interface gráfica avançada que permite filtrar e limpar dados intuitivamente. Destaca-se por incluir análises de  Predictive Power Score (PPS)  e  Time Series Analysis , permitindo uma visão preditiva precoce antes da modelagem formal.
sweetviz:  Focada em visualização comparativa automática, utilizando o  matplotlib  como motor para análise de densidade de variáveis com baixa intervenção manual.

# 8. Visualização de Dados como Suporte às Métricas
Bibliotecas como  Matplotlib  e  Seaborn  (Aula 01C) são indispensáveis para traduzir métricas abstratas em evidências visuais. Enquanto o IQR fornece um número, o  Boxplot  do Seaborn revela visualmente a presença de outliers e a assimetria da distribuição, permitindo uma compreensão holística que as estatísticas isoladas podem omitir.
