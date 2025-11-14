import argparse
import os
import time
import threading
from src.frequencias import gerar_tabela_frequencias, imprimir_tabela
from src.huffman_tree import construir_arvore, gerar_codigos, imprimir_arvore
from src.compressor import compactar, descompactar

# --- Variáveis Globais ---
arquivo_carregado = None
conteudo_arquivo = None
tabela_frequencias = None
raiz_huffman = None
codigos_huffman = None

# --- Funções de Lógica ---

def carregar_arquivo(caminho: str):
    """Carrega o conteúdo de um arquivo de texto."""
    global arquivo_carregado, conteudo_arquivo, tabela_frequencias, raiz_huffman, codigos_huffman
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            conteudo_arquivo = f.read()
        arquivo_carregado = caminho
        # Reseta as estruturas dependentes
        tabela_frequencias = None
        raiz_huffman = None
        codigos_huffman = None
        print(f"\nArquivo '{caminho}' carregado com sucesso.")
        return True
    except FileNotFoundError:
        print(f"\nErro: Arquivo '{caminho}' não encontrado.")
        return False
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")
        return False

def run_with_live_timer(message, func, *args):
    """
    Exibe uma animação de spinner e um cronômetro em tempo real enquanto a função 'func' é executada.
    Retorna a duração total da execução.
    """
    exception = None
    def target_wrapper():
        nonlocal exception
        try:
            func(*args)
        except Exception as e:
            exception = e

    thread = threading.Thread(target=target_wrapper)
    thread.start()

    start_time = time.time()
    spinner_chars = "||"
    idx = 0
    status_line = ""

    while thread.is_alive():
        elapsed_time = time.time() - start_time
        char = spinner_chars[idx % len(spinner_chars)]
        status_line = f" {message}... {char} ({elapsed_time:.2f}s)"
        print(status_line, end='\r')
        time.sleep(0.1)
        idx += 1
    
    thread.join()
    final_time = time.time() - start_time
    
    # Limpa a linha de status
    print(" " * (len(status_line) + 5), end='\r')

    if exception:
        raise exception
    
    return final_time

# --- Funções do Menu ---

def menu_gerar_tabela_freq():
    """Opção 2: Gera e imprime a tabela de frequências."""
    global tabela_frequencias
    print("\n--- Gerando Tabela de Frequências ---")
    if conteudo_arquivo is None:
        print("Erro: Nenhum arquivo carregado.")
        return
    
    if tabela_frequencias is None:
        print("Calculando frequências...")
        tabela_frequencias = gerar_tabela_frequencias(conteudo_arquivo)
    
    imprimir_tabela(tabela_frequencias)

def menu_gerar_arvore():
    """Opção 3: Gera e imprime a árvore de Huffman."""
    global raiz_huffman
    print("\n--- Gerando Árvore de Huffman ---")
    if tabela_frequencias is None:
        print("Tabela de frequências não gerada. Gerando agora...")
        menu_gerar_tabela_freq()
        print("\n--- Gerando Árvore de Huffman ---") # Repete o header para clareza

    if raiz_huffman is None:
        print("Construindo árvore...")
        raiz_huffman = construir_arvore(tabela_frequencias)
    
    imprimir_arvore(raiz_huffman)

def menu_gerar_codigos():
    """Opção 4: Gera e imprime os códigos de Huffman."""
    global codigos_huffman
    print("\n--- Gerando Tabela de Códigos ---")
    if raiz_huffman is None:
        print("Árvore de Huffman não gerada. Gerando agora...")
        menu_gerar_arvore()
        print("\n--- Gerando Tabela de Códigos ---") # Repete o header

    if codigos_huffman is None:
        print("Gerando códigos...")
        codigos_huffman = gerar_codigos(raiz_huffman)
    
    print("Caractere | Código")
    print("-------------------------")
    for char, codigo in sorted(codigos_huffman.items()):
        char_display = repr(char)[1:-1]
        if char == ' ':
            char_display = "' '"
        print(f"{char_display:<9} | {codigo}")
    print("-------------------------")

def menu_compactar():
    """Opção 5: Compacta o arquivo carregado."""
    print("\n--- Compactando Arquivo ---")
    if not arquivo_carregado:
        print("Erro: Nenhum arquivo carregado para compactar.")
        return

    nome_saida_base = input("Digite o nome para o arquivo de saída (deixe em branco para usar o nome original): ")

    # Garante que o arquivo de saída seja criado no mesmo diretório do arquivo de entrada
    dir_entrada = os.path.dirname(arquivo_carregado)
    if not dir_entrada:
        dir_entrada = '.' # Garante que funcione se o arquivo estiver no diretório atual

    if not nome_saida_base.strip():
        nome_base_original = os.path.basename(arquivo_carregado)
        nome_saida_base, _ = os.path.splitext(nome_base_original)

    arquivo_saida = os.path.join(dir_entrada, f"{nome_saida_base}.huff")

    try:
        print(f"Iniciando a compactação de '{os.path.basename(arquivo_carregado)}' para '{os.path.basename(arquivo_saida)}'...")
        duration = run_with_live_timer(
            "Compactando",
            compactar,
            arquivo_carregado,
            arquivo_saida
        )
        print(f"Arquivo '{arquivo_saida}' gerado com sucesso.")
        print(f"Tempo de execução: {duration:.4f} segundos.")
    except Exception as e:
        print(f"\nOcorreu um erro durante a compactação: {e}")

def menu_descompactar():
    """Opção 6: Descompacta um arquivo .huff."""
    print("\n--- Descompactando Arquivo ---")
    arquivo_entrada = input("Digite o caminho para o arquivo .huff: ")
    
    if not arquivo_entrada.endswith('.huff'):
        print("Erro: O arquivo de entrada deve ter a extensão .huff")
        return

    nome_base, _ = os.path.splitext(arquivo_entrada)
    arquivo_saida = f"{nome_base}_recuperado.txt"

    try:
        print(f"Iniciando a descompactação de '{os.path.basename(arquivo_entrada)}'...")
        duration = run_with_live_timer(
            "Descompactando",
            descompactar,
            arquivo_entrada,
            arquivo_saida
        )
        print(f"Arquivo '{arquivo_saida}' gerado com sucesso.")
        print(f"Tempo de execução: {duration:.4f} segundos.")
    except Exception as e:
        print(f"\nOcorreu um erro durante a descompactação: {e}")


def menu_ler_arquivo_texto():
    """Opção 1: Lê um arquivo de texto."""
    print("\n--- Leitura de Arquivo de Texto ---")
    caminho_arquivo = input("Digite o caminho para o arquivo de texto: ")
    carregar_arquivo(caminho_arquivo)

def mostrar_menu():
    """Exibe o menu principal e gerencia a entrada do usuário."""
    while True:
        print("\n--- Menu Principal ---")
        status_arquivo = f"Arquivo Carregado: {os.path.basename(arquivo_carregado)}" if arquivo_carregado else "Nenhum arquivo carregado"
        print(f"({status_arquivo})\n")
        print("1. Ler arquivo de texto")
        print("2. Gerar e imprimir tabela de frequências")
        print("3. Gerar e imprimir a árvore de Huffman")
        print("4. Gerar e imprimir tabela de códigos de Huffman")
        print("5. Compactar arquivo")
        print("6. Descompactar arquivo .huff")
        print("7. Sair")
        
        escolha = input("Escolha uma opção (1-7): ")
        
        if escolha == '1':
            menu_ler_arquivo_texto()
        elif escolha == '7':
            print("Saindo do programa.")
            break
        else:
            # Validação para outras opções que dependem de um arquivo carregado
            if arquivo_carregado is None and escolha not in ['6', '7']:
                print("\nErro: Por favor, carregue um arquivo primeiro (Opção 1).")
                continue
            
            if escolha == '2':
                menu_gerar_tabela_freq()
            elif escolha == '3':
                menu_gerar_arvore()
            elif escolha == '4':
                menu_gerar_codigos()
            elif escolha == '5':
                menu_compactar()
            elif escolha == '6':
                menu_descompactar()
            else:
                print("\nOpção inválida. Tente novamente.")

def main():
    """Função principal que inicializa o programa."""
    # Argument parser para --input
    parser = argparse.ArgumentParser(description="Compressor e Descompressor Huffman.")
    parser.add_argument("-i", "--input", help="Caminho do arquivo de texto para carregar inicialmente.")
    args = parser.parse_args()

    if args.input:
        if not carregar_arquivo(args.input):
            print("Não foi possível carregar o arquivo inicial fornecido via argumento.")
    
    mostrar_menu()

if __name__ == "__main__":
    main()
