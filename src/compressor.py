import json
from typing import Dict

from src.frequencias import gerar_tabela_frequencias
from src.huffman_tree import construir_arvore, gerar_codigos


def compactar(caminho_entrada: str, caminho_saida: str):
    """
    Lê um arquivo de texto, compacta seu conteúdo usando o algoritmo de Huffman
    e salva o resultado em um arquivo binário .huff.
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

    bits_compactados = _texto_para_bits(texto, codigos)
    dados_bytes = _empacotar_bits_em_bytes(bits_compactados)

    with open(caminho_saida, 'wb') as f:
        f.write(len(cabecalho_bytes).to_bytes(4, 'big'))
        f.write(cabecalho_bytes)
        f.write(dados_bytes)


def descompactar(caminho_entrada: str, caminho_saida: str):
    """
    Lê um arquivo .huff, descompacta seu conteúdo e salva o texto original.
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
            frequencias = json.loads(cabecalho_bytes.decode('utf-8'))
            dados_bytes = f.read()

    except (FileNotFoundError, json.JSONDecodeError, IndexError) as e:
        print(f"Erro ao ler o arquivo compactado: {e}")
        return

    bits_compactados = _desempacotar_bytes_em_bits(bytearray(dados_bytes))
    raiz = construir_arvore(frequencias)

    if not raiz:
        return

    texto_decodificado = []
    no_atual = raiz
    if not raiz.left and not raiz.right:
        texto_decodificado.append(raiz.char * raiz.freq)
    else:
        for bit in bits_compactados:
            no_atual = no_atual.left if bit == '0' else no_atual.right
            if no_atual.char is not None:
                texto_decodificado.append(no_atual.char)
                no_atual = raiz

    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.write("".join(texto_decodificado))

def _texto_para_bits(texto: str, codigos: Dict[str, str]) -> str:
    """Converte o texto em uma string de bits usando a tabela de códigos."""
    return "".join(codigos[char] for char in texto)

def _empacotar_bits_em_bytes(bits: str) -> bytearray:
    """Converte uma string de bits em bytes, adicionando padding info."""
    padding_len = (8 - len(bits) % 8) % 8
    bits_com_padding = bits + '0' * padding_len
    info_padding = f'{padding_len:08b}'
    bits_final = info_padding + bits_com_padding

    b = bytearray()
    for i in range(0, len(bits_final), 8):
        b.append(int(bits_final[i:i+8], 2))
    return b

def _desempacotar_bytes_em_bits(data: bytearray) -> str:
    """Converte bytes de volta para uma string de bits, removendo o padding."""
    if not data:
        return ""
    
    bits = "".join(f'{byte:08b}' for byte in data)
    padding_len = int(bits[:8], 2)
    bits_sem_info = bits[8:]
    
    if padding_len > 0:
        return bits_sem_info[:-padding_len]
    return bits_sem_info
