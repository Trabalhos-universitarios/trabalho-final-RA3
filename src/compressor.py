import json
from typing import Dict, Iterator

from src.frequencias import gerar_tabela_frequencias
from src.huffman_tree import construir_arvore, gerar_codigos


def compactar(caminho_entrada: str, caminho_saida: str):
    """
    Lê um arquivo de texto, compacta seu conteúdo usando o algoritmo de Huffman
    e salva o resultado em um arquivo binário .huff.
    Versão otimizada que não cria uma string de bits gigante em memória.
    """
    try:
        with open(caminho_entrada, 'r', encoding='utf-8') as f:
            texto = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo de entrada '{caminho_entrada}' não encontrado.")
        return

    if not texto:
        with open(caminho_saida, 'wb') as f:
            f.write(b'')
        return

    frequencias = gerar_tabela_frequencias(texto)
    raiz = construir_arvore(frequencias)
    codigos = gerar_codigos(raiz)

    cabecalho_json = json.dumps(frequencias)
    cabecalho_bytes = cabecalho_json.encode('utf-8')

    with open(caminho_saida, 'wb') as f:
        # Escreve o cabeçalho
        f.write(len(cabecalho_bytes).to_bytes(4, 'big'))
        f.write(cabecalho_bytes)

        # Escreve os dados compactados de forma eficiente
        bit_buffer = ""
        for char in texto:
            bit_buffer += codigos[char]
            while len(bit_buffer) >= 8:
                byte_str = bit_buffer[:8]
                f.write(int(byte_str, 2).to_bytes(1, 'big'))
                bit_buffer = bit_buffer[8:]
        
        # Trata o padding no final
        if bit_buffer:
            padding_len = 8 - len(bit_buffer)
            bit_buffer += '0' * padding_len
            # O último byte contém a informação de padding no seu valor
            # A decodificação precisa saber o número total de bits
            f.write(int(bit_buffer, 2).to_bytes(1, 'big'))
    
    # Para a descompactação funcionar, ela precisa saber o número exato de bits
    # ou o número de caracteres originais. Vamos adicionar o número de caracteres
    # ao cabeçalho, que é uma abordagem mais robusta.

    # --- REFAZENDO A COMPACTAÇÃO COM A ABORDAGEM CORRETA ---

    # O cabeçalho precisa conter as frequências E o número de caracteres
    header_data = {
        'frequencias': frequencias,
        'total_chars': len(texto)
    }
    cabecalho_json = json.dumps(header_data)
    cabecalho_bytes = cabecalho_json.encode('utf-8')

    with open(caminho_saida, 'wb') as f:
        f.write(len(cabecalho_bytes).to_bytes(4, 'big'))
        f.write(cabecalho_bytes)

        bit_buffer = ""
        for char in texto:
            bit_buffer += codigos[char]
            while len(bit_buffer) >= 8:
                byte = int(bit_buffer[:8], 2)
                f.write(byte.to_bytes(1, 'big'))
                bit_buffer = bit_buffer[8:]
        
        # Escreve o último byte, se houver bits restantes
        if bit_buffer:
            byte = int(bit_buffer.ljust(8, '0'), 2)
            f.write(byte.to_bytes(1, 'big'))


def descompactar(caminho_entrada: str, caminho_saida: str):
    """
    Lê um arquivo .huff, descompacta seu conteúdo e salva o texto original.
    Versão ajustada para ler o novo formato de cabeçalho.
    """
    try:
        with open(caminho_entrada, 'rb') as f:
            tamanho_cabecalho_bytes = f.read(4)
            if not tamanho_cabecalho_bytes:
                with open(caminho_saida, 'w', encoding='utf-8') as f_out:
                    f_out.write("")
                return

            tamanho_cabecalho = int.from_bytes(tamanho_cabecalho_bytes, 'big')
            cabecalho_bytes = f.read(tamanho_cabecalho)
            header_data = json.loads(cabecalho_bytes.decode('utf-8'))
            frequencias = header_data['frequencias']
            total_chars = header_data['total_chars']
            
            dados_bytes = f.read()

    except (FileNotFoundError, json.JSONDecodeError, IndexError, KeyError) as e:
        # Imprime o erro para feedback imediato, mas também o relança
        # para que a função que chamou saiba que a operação falhou.
        print(f"Erro ao ler o arquivo compactado: {e}")
        raise

    raiz = construir_arvore(frequencias)
    if not raiz:
        if total_chars > 0:
             print("Erro: Árvore de Huffman vazia mas o arquivo não deveria estar vazio.")
        return

    texto_decodificado = []
    char_count = 0
    
    # Caso especial: arquivo com um único tipo de caractere repetido
    if not raiz.left and not raiz.right:
        texto_decodificado.append(raiz.char * total_chars)
    else:
        no_atual = raiz
        for byte in dados_bytes:
            bits = f'{byte:08b}'
            for bit in bits:
                if char_count >= total_chars:
                    break
                
                no_atual = no_atual.left if bit == '0' else no_atual.right
                if no_atual.char is not None:
                    texto_decodificado.append(no_atual.char)
                    char_count += 1
                    no_atual = raiz
            if char_count >= total_chars:
                break

    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.write("".join(texto_decodificado))

# --- Funções auxiliares antigas removidas para dar lugar a uma lógica integrada ---
# As funções _texto_para_bits, _empacotar_bits_em_bytes, e _desempacotar_bytes_em_bits
# foram substituídas pela lógica direta e mais eficiente dentro de compactar e descompactar.
