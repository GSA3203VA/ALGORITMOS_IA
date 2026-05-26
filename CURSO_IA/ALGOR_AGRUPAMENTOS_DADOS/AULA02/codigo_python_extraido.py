# ===== CÓDIGO 1 =====
from
 
sklearn.datasets
 
import
 
make_blobs



# criando dados


data
,
 
labels
 
=
 
make_blobs
(
n_samples
=
200
,
 
n_features
=
2
,
 
centers
=
5
,
 
cluster_std
=
1
,
 
random_state
=
150
)


plt
.
scatter
(
data
[:,
0
],
 
data
[:,
1
],
 
c
=
labels
,
cmap
=
'rainbow'
)

# ===== CÓDIGO 2 =====
from
 
sklearn.cluster
 
import
 
KMeans


wcss
 
=
 
[]


for
 
i
 
in
 
range
 
(
1
,
11
):

    
kmeans
 
=
 
KMeans
(
n_clusters
 
=
 
i
,
 
init
 
=
 
'k-means++'
,
 
random_state
 
=
 
150
)

    
kmeans
.
fit
(
data
)

    
wcss
.
append
(
kmeans
.
inertia_
)


plt
.
plot
(
range
(
1
,
11
),
 
wcss
,
 
color
=
'k'
)


plt
.
title
(
'A Curva do Cotovelo do Algoritmo k-means'
)


plt
.
xlabel
(
'Número de Clusters (k)'
)


plt
.
ylabel
(
'Soma dos Quadrados do Cluster (wcss)'
)


plt
.
show
()

# ===== CÓDIGO 3 =====
from
 
sklearn.cluster
 
import
 
KMeans


kmeans
 
=
 
KMeans
(
n_clusters
=
5
,
 
init
=
'k-means++'
)


kmeans
.
fit
(
data
)

# ===== CÓDIGO 4 =====
f
,
 
(
ax1
,
 
ax2
)
 
=
 
plt
.
subplots
(
1
,
 
2
,
 
sharey
=
True
,
 
figsize
=
(
10
,
6
))


ax1
.
set_title
(
'K-means'
)


ax1
.
scatter
(
data
[:,
0
],
data
[:,
1
],
c
=
kmeans
.
labels_
,
cmap
=
'rainbow'
)


ax2
.
set_title
(
'Original'
)


ax2
.
scatter
(
data
[:,
0
],
data
[:,
1
],
c
=
labels
,
cmap
=
'rainbow'
)

