from collections import deque

class BST:
  def __init__(self):
    self.raiz = None
    
  def inserir(self, valor):
    self.raiz = self._inserir(self.raiz, valor)

  def _inserir(self, nodo, valor):
    if nodo is None:
      return Nodo(valor)
    if valor < nodo.valor:
      nodo.esquerda = self._inserir(nodo.esquerda, valor)
    elif valor > nodo.valor:
      nodo.direita = self._inserir(nodo.direita, valor)
    return nodo

  def imprimir(self):
    if self.raiz is None:
        print("(árvore vazia)")
        return
    print(str(self.raiz.valor))
    self._imprimir(self.raiz.esquerda, "e:")
    self._imprimir(self.raiz.direita,  "d:")
    
  def _imprimir(self, nodo, indentacao):
      if nodo is None:
          return
      
      indentacao += "--"
      print(indentacao + str(nodo.valor))

      self._imprimir(nodo.esquerda, indentacao + "e:")
      self._imprimir(nodo.direita,  indentacao + "d:")
      
  def remover(self, valor):
    print(f"(remover) valor: {valor}")
    self.raiz = self._remover(self.raiz, valor)

  def _remover(self, nodo, valor):
    if nodo is None:
       return None
    if valor < nodo.valor:
      nodo.esquerda = self._remover(nodo.esquerda, valor)
    elif valor > nodo.valor:
      nodo.direita = self._remover(nodo.direita, valor)
    else:
      if nodo.esquerda is None:        
        return nodo.direita
      if nodo.direita is None:
        return nodo.esquerda
        
      sucessor = self._minimo(nodo.direita)
      nodo.valor = sucessor.valor
      nodo.direita = self._remover(nodo.direita, sucessor.valor)
    return nodo
    
  def _minimo(self, nodo):
    while nodo.esquerda:
      nodo = nodo.esquerda
    return nodo
    
  def buscar(self, valor):
    return self._buscar(self.raiz, valor)

  def _buscar(self, nodo, valor):
    if nodo is None:
      return False
    if valor == nodo.valor:
      return True
     
    if valor < nodo.valor:
      return self._buscar(nodo.esquerda, valor)
    else:
      return self._buscar(nodo.direita, valor)        
  
  def listar_infix(self):
      if (self.raiz is None):
        return ""
      else:
        return self._listar_infix(self.raiz)
    
  def _listar_infix(self, nodo):
      if (nodo.esquerda is None and nodo.direita is None):
        return nodo.valor
      esquerda = self._listar_infix(nodo.esquerda)
      direita = self._listar_infix(nodo.direita)
      return f"{esquerda} {nodo.valor} {direita}"

  def listar_posfix(self):
      if (self.raiz is None):
        return ""
      else:
        return [self._listar_infix(self.raiz)]
    
  def _listar_posfix(self, nodo):
      if (nodo.esquerda is None and nodo.direita is None):
        return str(nodo.valor)
      esquerda = self._listar_infix(nodo.esquerda)
      direita = self._listar_infix(nodo.direita)
      return f"{esquerda} {nodo.valor} {direita}"
      
  def asc(self):
    self._asc(self.raiz)

  def _asc(self, nodo):
    if(nodo.esquerda != None):
      self._asc(nodo.esquerda)
    print(nodo.valor)
    
    if(nodo.direita != None):
      self._asc(nodo.direita)

  def desc(self):
    self._desc(self.raiz)

  def _desc(self, nodo):
    if(nodo.direita != None):
      self._desc(nodo.direita)
    print(nodo.valor)
    if(nodo.esquerda != None):
      self._desc(nodo.esquerda)

  def vetor_posfix(self):
    resultado = []
    self._vetor_posfix(self.raiz, resultado)
    return resultado

  def _vetor_posfix(self, nodo, resultado):
    if (nodo):
      self._vetor_posfix(nodo.esquerda, resultado)
      self._vetor_posfix(nodo.direita, resultado)
      resultado.append(nodo.valor)
      
  def RunBFS(self):
    if self.raiz is None:
      print("Árvore vazia")
      return []

    valuesInBFSOrder = []
    queue = deque()
    queue.append(self.raiz)
    
    while(len(queue) > 0):
      node = queue.popleft()
      valuesInBFSOrder.append(node.valor)

      if node.esquerda is not None:
        queue.append(node.esquerda)
      if node.direita is not None:
        queue.append(node.direita)

      print(valuesInBFSOrder)

    return valuesInBFSOrder
        
  def bfs_recursivo(self):
    stop = False
    depth = 0
    while(not stop):
      this_depth_nodes = self._bfs(self.raiz, 0, depth)
      if(len(this_depth_nodes) > 0):
        print(this_depth_nodes)
        depth += 1
      else:
        stop = True

  def _bfs(self, node, this_depth, target_depth):
    acc = []
    if(this_depth == target_depth):
      return [node.valor]
    if(this_depth < target_depth):
      if(node.esquerda != None):
        acc += self._bfs(node.esquerda, this_depth+1, target_depth)
      if(node.direita != None):
        acc += self._bfs(node.direita, this_depth+1, target_depth)
    return acc

class Nodo:
  def __init__(self, valor):
    self.valor = valor
    self.esquerda = None
    self.direita = None

minhaArvore = BST()

for i in ([50, 30, 70, 20, 40, 60, 80]):
    minhaArvore.inserir(i)

minhaArvore.imprimir()


#print(minhaArvore.RunBFS())

minhaArvore.bfs_iterativa()
