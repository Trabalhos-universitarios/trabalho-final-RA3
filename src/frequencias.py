
from collections import Counter
import operator

def gerar_tabela_frequencias(texto: str) -> dict[str, int]:
    """
    Gera uma tabela de frequências de caracteres a partir de um texto.

    Args:
        texto: O texto de entrada.

    Returns:
        Um dicionário com os caracteres e suas frequências,
        ordenado alfabeticamente.
    """
    # Conta a frequência de cada caractere
    frequencias = Counter(texto)
    
    # Ordena o dicionário pela chave (caractere) em ordem alfabética
    frequencias_ordenadas = dict(sorted(frequencias.items(), key=operator.itemgetter(0)))
    
    return frequencias_ordenadas

def imprimir_tabela(frequencias: dict[str, int]):
    """
    Imprime a tabela de frequências de forma legível no console.

    Args:
        frequencias: O dicionário de frequências.
    """
    print("--- Tabela de Frequências ---")
    print("Caractere | Frequência")
    print("---------------------------")
    for char, freq in frequencias.items():
        # Trata caracteres especiais para exibição
        char_display = repr(char)[1:-1]
        if char == ' ':
            char_display = "' '"
        print(f"{char_display:<9} | {freq}")
    print("---------------------------")

