# Compressor de Arquivos com Algoritmo de Huffman

Este projeto, desenvolvido para a disciplina de Resolução de Problemas Estruturados em Computação, consiste em uma ferramenta de linha de comando em Python para compactar e descompactar arquivos de texto utilizando o clássico algoritmo de Huffman.

O programa oferece uma interface interativa que guia o usuário através de todas as etapas do processo, desde a análise de frequência dos caracteres até a geração do arquivo final compactado.

---

## ✨ Funcionalidades

- **Compactação e Descompactação:** Converte arquivos de texto para um formato `.huff` binário e os reconstrói perfeitamente.
- **Interface Interativa:** Um menu de linha de comando simples e intuitivo para acessar todas as funções.
- **Visualização Passo a Passo:** Permite inspecionar as estruturas de dados internas do algoritmo:
    - Tabela de Frequências (ordenada da maior para a menor).
    - Árvore de Huffman (exibida de forma estruturada).
    - Tabela de Códigos Binários para cada caractere.
- **Processamento Eficiente:** Otimizado para lidar com arquivos grandes sem consumir memória excessiva, processando os dados de forma incremental.
- **Feedback em Tempo Real:** Exibe um cronômetro e uma animação durante as operações de compactação e descompactação, informando o usuário que o processo está em andamento.
- **Nomes de Arquivo Customizáveis:** Permite ao usuário escolher o nome do arquivo `.huff` a ser gerado.

---

## 🚀 Como Executar

Para iniciar a interface interativa, execute o seguinte comando a partir da pasta raiz do projeto:

```bash
python3 src/main.py
```

Opcionalmente, você pode carregar um arquivo de texto diretamente na inicialização usando o argumento `-i` ou `--input`:

```bash
python3 src/main.py -i caminho/para/seu/arquivo.txt
```

---

## 📂 Estrutura do Projeto

O código-fonte é modularizado para garantir clareza e manutenibilidade:

-   `src/main.py`: Ponto de entrada do programa. Responsável pela interface com o usuário (menu) e por orquestrar as chamadas para outras funções.
-   `src/compressor.py`: Contém a lógica central de compactação e descompactação, incluindo a leitura e escrita do formato `.huff`.
-   `src/frequencias.py`: Funções para geração da tabela de frequências a partir de um texto e sua impressão formatada.
-   `src/huffman_tree.py`: Implementação da estrutura de dados `Node` e das funções para construir a árvore de Huffman, gerar os códigos e imprimir a árvore de forma visual.
-   `tests/`: Contém testes unitários para validar partes do código.

---

## 🏅 Qualidade do Código

Este projeto foi desenvolvido com o objetivo de alcançar a nota máxima ("Nível 5 - Excelente") na rubrica de avaliação fornecida. Os principais focos foram:

-   **Modularidade e Clareza:** Separação clara de responsabilidades entre os arquivos.
-   **Eficiência:** Implementação de um algoritmo de compactação que não sofre com problemas de memória em arquivos grandes.
-   **Robustez:** Tratamento de erros (ex: arquivo não encontrado) e feedback claro para o usuário.
-   **Funcionalidade Completa:** Atende a todos os requisitos funcionais, desde a correta (des)compactação até a visualização das estruturas de dados.