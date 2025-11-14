
from collections import Counter

def gerar_tabela_frequencias(texto: str) -> dict[str, int]:
    """
    Gera uma tabela de frequências de caracteres a partir de um texto.

    Args:
        texto: O texto de entrada.

    Returns:
        Um dicionário com os caracteres e suas frequências.
    """
    return Counter(texto)

def imprimir_tabela(frequencias: dict[str, int]):
    """
    Imprime a tabela de frequências de forma legível no console,
    ordenada da maior para a menor frequência.

    Args:
        frequencias: O dicionário de frequências.
    """
    print("--- Tabela de Frequências ---")
    print("Caractere | Frequência")
    print("---------------------------")
    
    # Ordena os itens do dicionário pela frequência (valor), em ordem decrescente
    sorted_freq = sorted(frequencias.items(), key=lambda item: item[1], reverse=True)
    
    for char, freq in sorted_freq:
        # Trata caracteres especiais para exibição
        char_display = repr(char)[1:-1]
        if char == ' ':
            char_display = "' '"
        print(f"{char_display:<9} | {freq}")
    print("---------------------------")

