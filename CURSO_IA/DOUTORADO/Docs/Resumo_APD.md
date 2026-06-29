## Resumo da Disciplina: Algoritmos para Agrupamento de Dados
# 1. Introdução ao Agrupamento de Dados (Clustering)
O agrupamento de dados, ou  clustering , é uma técnica fundamental da  Aprendizagem Não Supervisionada  (Reconhecimento de Modelos) cujo objetivo principal é identificar padrões, modelos ou grupos de objetos similares em um conjunto de dados multidimensionais sem a necessidade de rótulos prévios. Esta metodologia é vital para a Mineração de Dados ( Datamining ) contemporânea, pois a capacidade humana de processar e extrair conhecimento em bases de dados "gigantes" é limitada, tornando a automação do agrupamento indispensável para a descoberta de conhecimento.Conforme apresentado em nossa disciplina, o impacto do clustering abrange diversos domínios:
Câncer:  Classificação de pacientes em subgrupos com base no perfil genético para compreender a progressão da doença e refinar o prognóstico.
Marketing:  Segmentação de mercados através da identificação de subgrupos de consumidores com perfis similares, otimizando a receptividade a campanhas publicitárias específicas.
Planejamento Urbano:  Agrupamento de residências considerando atributos essenciais como tipo, valor e localização geográfica para subsidiar decisões de infraestrutura.

# 2. Conceitos Fundamentais de Similaridade e o Algoritmo k-NN
A espinha dorsal de qualquer algoritmo de agrupamento é a definição de uma métrica de similaridade. Sem uma forma matemática de quantificar quão próximos dois objetos estão em um espaço de atributos, torna-se impossível formar grupos coesos. No e-commerce, por exemplo, a similaridade baseada no histórico de compras permite que o sistema identifique modelos de consumo e ofereça sugestões personalizadas.
Pseudocódigo do Algoritmo k-NN (k-Nearest Neighbors)
O k-NN é um classificador baseado em instâncias que segue esta lógica fundamental:
Supor a existência de alguma métrica para avaliar a similaridade entre atributos de um dado vetor. Seja  $\mathbf{x}$  o objeto cuja classe/grupo esperamos determinar.
Entre os exemplos de treinamento (dados), identificar os  k  vizinhos mais próximos a  $\mathbf{x}$  (os exemplos mais similares).
Identificar a classe  $c_i$  mais frequentemente encontrada entre esses  k  vizinhos mais próximos.
Rotular o objeto  $\mathbf{x}$  com a classe  $c_i$ .
Métricas de Similaridade Matemáticas
A escolha da métrica define a topologia do espaço de busca. As principais métricas utilizadas são:
Distância Euclidiana:  Procedimento clássico que mede a distância direta entre dois pontos. No plano 2D, para  $\mathbf{x} = (x_1, x_2)$  e  $\mathbf{y} = (y_1, y_2)$ :  $$d_E(\mathbf{x}, \mathbf{y}) = \sqrt{(x_1 - y_1)^2 + (x_2 - y_2)^2}$$  Para  $n$  dimensões, a fórmula generalizada é:  $$d_E(\mathbf{x}, \mathbf{y}) = \sqrt{\sum_{i=1}^{n} (x_i - y_i)^2}$$
Distância Manhattan (City Block):  Mede a distância percorrendo apenas eixos ortogonais, simulando o trajeto entre quarteirões. Sua fórmula é:  $$d_M(\mathbf{x}, \mathbf{y}) = \sum_{i=1}^{n} |x_i - y_i|$$
Impacto do Hiperparâmetro k e do Ruído
A escolha de  k  é um exercício de equilíbrio entre viés e variância. Um valor de  $k=1$  é extremamente sensível a ruídos; se um dado estiver corrompido, o classificador falhará. Ao aumentarmos o valor para  $k=3$ , introduzimos um "efeito de suavização" na fronteira de decisão, permitindo que o consenso da vizinhança ignore  outliers  isolados. É importante notar a existência da "terra de ninguém": regiões  borderline  onde a classificação não é confiável devido à proximidade equitativa entre diferentes grupos.

# 3. Métodos Particionais e Hierárquicos: Uma Visão Comparativa
Os algoritmos podem ser divididos entre aqueles que buscam partições globais e aqueles que constroem estruturas de árvore (dendrogramas). Em nossos experimentos práticos, observamos que métodos como o  K-means  e o  Hierárquico Aglomerativo (Linkage Ward)  tendem a favorecer clusters compactos e convexos. Em contrapartida, o  Hierárquico Aglomerativo (Linkage Single)  compartilha uma característica com o DBSCAN: a capacidade de seguir "cadeias" de similaridade para identificar formas complexas.| Característica | Métodos Particionais / Hierárquicos (K-means, Ward) | DBSCAN / Hierárquico (Single) || ------ | ------ | ------ || Tipo de Cluster | Clusters esféricos ou convexos. | Formas aleatórias e arbitrárias. || Sensibilidade a Ruído | Alta (impactados por outliers). | Baixa (robusto a ruídos). || Número de Clusters | Necessidade de definição prévia. | Identificação automática. |

# 4. Agrupamento Baseado em Densidade: DBSCAN
O DBSCAN ( Density-Based Spatial Clustering of Applications with Noise ) opera sob a premissa de que clusters são regiões de alta densidade separadas por regiões de baixa densidade. Diferente do K-means, ele não tenta acomodar todos os pontos em grupos, permitindo a identificação explícita de ruído.O algoritmo classifica os pontos em três categorias:
Pontos Centrais (Core):  Possuem o número mínimo de vizinhos dentro do raio definido.
Pontos de Borda (Border):  Estão dentro do raio de um ponto central, mas não possuem densidade suficiente para serem centros.
Ruído (Noise):  Pontos que não pertencem a nenhuma das categorias anteriores.Para este cálculo, o especialista deve ajustar dois parâmetros fundamentais:
Raio (  $\epsilon$  - epsilon):  A distância máxima para definir a vizinhança.
Número mínimo de dados (  $Num\_min$  ):  A quantidade mínima de pontos (incluindo o próprio ponto) para caracterizar uma região como densa.Sua maior vantagem é a capacidade de gerar clusters de formas não convexas e o tratamento automático de  outliers , o que o torna superior em bases de dados ruidosas.

# 5. Panorama das Atividades Práticas (Laboratórios 01 e 04)
LAB01 (k-NN)
Este laboratório focou na aplicação prática utilizando a biblioteca  scikit-learn .
Bases de Dados:  Utilizamos o  heart.csv  (doenças cardíacas),  cliente.csv  (analisando renda/income e pontuação de crédito/score para pedidos de empréstimo) e o  RHdataset.xls .
Insights Pedagógicos:  No dataset de RH (com 10 atributos de entrada como "Porcentagem de iniciativa" e "Capacidade de resposta"), reforçamos que a  normalização  é uma "boa prática" indispensável; mesmo quando os dados já estão em uma escala comum (porcentagens), a normalização mantém a consistência do  pipeline  de dados.
Configuração Experimental:  Aplicamos uma divisão de  70% para treinamento e 30% para teste , utilizando gráficos de erro para determinar o  $k$  ideal.
LAB04 (DBSCAN)
Focado na análise comparativa de paradigmas de agrupamento.
Experimentos Sintéticos:  Através das funções  make_moons  (formato de meia-lua) e  make_blobs , ficou evidente que o K-means e o Agrupamento Hierárquico (Ward) falham em capturar formas não convexas, enquanto o DBSCAN e o Hierárquico ( Single Linkage ) obtêm sucesso.
Variação de Hiperparâmetros:  Testamos o impacto do raio de vizinhança com valores de  $\epsilon = 0.2$ ,  $0.7$  e  $4.0$ . Observou-se que um  $\epsilon$  muito pequeno (0.2) pode fragmentar excessivamente os dados ou considerar tudo como ruído, enquanto um  $\epsilon$  muito grande (4.0) pode fundir todos os pontos em um único cluster global, perdendo o poder de discriminação.

#6. Conclusão e Métricas de Avaliação
A eficácia de um algoritmo de agrupamento não é absoluta, mas sim dependente do contexto e da morfologia dos dados. Para validar os resultados, utilizamos métricas de avaliação que podem ser supervisionadas (quando há um rótulo de referência) ou não supervisionadas (avaliando a coesão interna e separação dos clusters).Como especialistas, devemos sempre priorizar a  normalização dos dados  para garantir que atributos com escalas diferentes não distorçam a métrica de distância, além de realizar um  ajuste fino de hiperparâmetros  ( $k$  ou  $\epsilon$ ). O sucesso em problemas do mundo real reside na escolha do algoritmo que melhor se adapta à densidade e geometria da base de dados minerada.

