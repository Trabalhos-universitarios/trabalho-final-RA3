=====================================================
Algoritmo de Huffman - Compressão/Descompressão
=====================================================

Projeto desenvolvido para a disciplina de Resolução de Problemas Estruturados em Computação.

---

## Como Executar o Programa

Para iniciar a interface interativa, execute o seguinte comando a partir da pasta raiz do projeto:

```
python3 -m src.main
```

Opcionalmente, você pode carregar um arquivo de texto diretamente na inicialização usando o argumento `--input`:

```
python3 -m src.main --input caminho/para/seu/arquivo.txt
```

---

## Como Usar o Menu Interativo

O programa apresentará um menu com as seguintes opções:

1.  **Ler arquivo de texto**: Carrega um arquivo .txt na memória. Este é o primeiro passo para a maioria das operações.
2.  **Gerar e imprimir tabela de frequências**: Mostra a contagem de cada caractere no arquivo carregado.
3.  **Gerar e imprimir a árvore de Huffman**: Mostra a estrutura da árvore gerada a partir das frequências.
4.  **Gerar e imprimir tabela de códigos de Huffman**: Exibe o código binário para cada caractere.
5.  **Compactar arquivo**: Cria uma versão `.huff` do arquivo carregado. O arquivo de saída será salvo na mesma pasta do original.
6.  **Descompactar arquivo .huff**: Pede o caminho de um arquivo `.huff` e cria a sua versão original (`_recuperado.txt`).
7.  **Sair**: Encerra o programa.

---

## Arquivos Inclusos

- `exemplo.txt`: Um pequeno arquivo de texto para testes rápidos.
- `src/`: Pasta contendo todo o código-fonte do projeto, dividido em módulos.
- `tests/`: Pasta contendo testes unitários.
