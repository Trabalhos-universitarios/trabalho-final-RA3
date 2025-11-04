
import heapq
import json
from typing import Optional, Dict, List, Union

# --- Estrutura do Nó e da Árvore ---

class Node:
    """Nó da árvore de Huffman."""
    def __init__(self, char: Optional[str], freq: int):
        self.char = char
        self.freq = freq
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    # Métodos de comparação para que o heapq funcione corretamente
    def __lt__(self, other: "Node") -> bool:
        return self.freq < other.freq

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.freq == other.freq

# --- Funções Principais ---

def construir_arvore(frequencias: Dict[str, int]) -> Optional[Node]:
    """Constrói a árvore de Huffman a partir da tabela de frequências."""
    if not frequencias:
        return None

    # 1. Cria a fila de prioridade com os nós folha
    fila_prioridade = [Node(char, freq) for char, freq in frequencias.items()]
    heapq.heapify(fila_prioridade)

    # 3. Combina os nós até restar apenas um (a raiz)
    while len(fila_prioridade) > 1:
        # 3a. Remove os dois nós de menor frequência
        no_esquerdo = heapq.heappop(fila_prioridade)
        no_direito = heapq.heappop(fila_prioridade)

        # 3b. Cria um nó interno com a soma das frequências
        freq_soma = no_esquerdo.freq + no_direito.freq
        no_pai = Node(None, freq_soma)
        no_pai.left = no_esquerdo
        no_pai.right = no_direito

        # 3d. Adiciona o novo nó de volta à fila
        heapq.heappush(fila_prioridade, no_pai)

    # 4. A raiz da árvore é o único nó que restou
    return fila_prioridade[0] if fila_prioridade else None

def gerar_codigos(raiz: Optional[Node]) -> Dict[str, str]:
    """Gera os códigos de Huffman para cada caractere a partir da árvore."""
    codigos: Dict[str, str] = {}

    def _percorrer(no: Optional[Node], codigo_atual: str):
        if no is None:
            return

        # Se o nó é uma folha, armazena o código para o caractere
        if no.char is not None:
            # Caso especial: árvore com um único nó
            if not codigo_atual:
                codigos[no.char] = "0"
            else:
                codigos[no.char] = codigo_atual
            return

        # Percorre para a esquerda (adiciona '0') e para a direita (adiciona '1')
        _percorrer(no.left, codigo_atual + "0")
        _percorrer(no.right, codigo_atual + "1")

    _percorrer(raiz, "")
    return codigos

def imprimir_arvore(raiz: Optional[Node], prefixo="", is_ultimo=True):
    """Imprime a estrutura da árvore de Huffman de forma visual."""
    if raiz is not None:
        print(prefixo, end="")
        if is_ultimo:
            print("└── ", end="")
            prefixo += "    "
        else:
            print("├── ", end="")
            prefixo += "|   "

        char_repr = f"'{raiz.char}'" if raiz.char is not None else "[I]"
        print(f"{char_repr} ({raiz.freq})")

        # A árvore de Huffman pode ter filhos em qualquer ordem, mas para uma impressão
        # consistente, podemos tratar a impressão de múltiplos filhos.
        # Neste caso, são sempre 2 ou 0 filhos.
        if raiz.left is not None or raiz.right is not None:
            # Imprime o filho direito primeiro se o esquerdo também existir
            if raiz.right and raiz.left:
                imprimir_arvore(raiz.right, prefixo, False)
                imprimir_arvore(raiz.left, prefixo, True)
            # Caso tenha apenas um filho (não deveria acontecer em Huffman, mas por robustez)
            elif raiz.right:
                imprimir_arvore(raiz.right, prefixo, True)
            elif raiz.left:
                imprimir_arvore(raiz.left, prefixo, True)

# --- Serialização ---

def serializar_tabela(frequencias: Dict[str, int]) -> str:
    """Serializa a tabela de frequências para JSON."""
    return json.dumps(frequencias)

def deserializar_tabela(data: str) -> Dict[str, int]:
    """Deserializa a tabela de frequências a partir de JSON."""
    return json.loads(data)

