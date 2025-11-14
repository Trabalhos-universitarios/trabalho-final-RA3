
import unittest
import os
import tempfile
from src.frequencias import gerar_tabela_frequencias
from src.huffman_tree import construir_arvore, gerar_codigos
from src.compressor import compactar, descompactar

class TestHuffmanTree(unittest.TestCase):
    """Testes para a lógica de construção da árvore e geração de códigos."""

    def test_gerar_codigos_propriedades(self):
        """Verifica se os códigos gerados são prefix-free e se os mais frequentes são mais curtos."""
        frequencias = {'a': 10, 'b': 5, 'c': 2, 'd': 1}
        raiz = construir_arvore(frequencias)
        codigos = gerar_codigos(raiz)

        # O caractere mais frequente ('a') deve ter o código mais curto
        self.assertEqual(len(codigos['a']), 1)

        # O caractere menos frequente ('d') deve ter o código mais longo
        self.assertEqual(len(codigos['d']), 3)

        # Propriedade Prefix-Free: Nenhum código pode ser o prefixo de outro
        lista_codigos = list(codigos.values())
        for i, codigo1 in enumerate(lista_codigos):
            for j, codigo2 in enumerate(lista_codigos):
                if i != j:
                    self.assertFalse(codigo2.startswith(codigo1), f"{codigo1} é prefixo de {codigo2}")

    def test_caso_especial_um_caractere(self):
        """Testa o caso de um arquivo com apenas um tipo de caractere."""
        frequencias = {'a': 100}
        raiz = construir_arvore(frequencias)
        codigos = gerar_codigos(raiz)
        self.assertEqual(codigos['a'], "0")


class TestCompressorIntegration(unittest.TestCase):
    """Teste de integração para o ciclo completo de compactar e descompactar."""

    def setUp(self):
        """Cria arquivos temporários para os testes."""
        # Usamos NamedTemporaryFile para que o sistema operacional gerencie a exclusão
        self.arquivo_original = tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8')
        self.arquivo_compactado = tempfile.NamedTemporaryFile(delete=False)
        self.arquivo_recuperado = tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8')
        
        self.lista_arquivos = [
            self.arquivo_original.name,
            self.arquivo_compactado.name,
            self.arquivo_recuperado.name
        ]

    def tearDown(self):
        """Fecha e remove os arquivos temporários."""
        self.arquivo_original.close()
        self.arquivo_compactado.close()
        self.arquivo_recuperado.close()
        for arquivo in self.lista_arquivos:
            os.remove(arquivo)

    def test_ciclo_completo(self):
        """Testa se um arquivo descompactado é idêntico ao original."""
        texto_original = "o algoritmo de huffman é um algoritmo de compressão usado para compactar dados, baseando-se na frequência de cada caractere."
        
        # Escreve no arquivo original e volta ao início para leitura futura se necessário
        self.arquivo_original.write(texto_original)
        self.arquivo_original.seek(0)

        # Roda o ciclo
        compactar(self.arquivo_original.name, self.arquivo_compactado.name)
        descompactar(self.arquivo_compactado.name, self.arquivo_recuperado.name)

        # Lê o resultado
        self.arquivo_recuperado.seek(0)
        texto_recuperado = self.arquivo_recuperado.read()

        self.assertEqual(texto_original, texto_recuperado)

    def test_ciclo_arquivo_vazio(self):
        """Testa se o ciclo funciona corretamente para um arquivo vazio."""
        texto_original = ""
        self.arquivo_original.write(texto_original)
        self.arquivo_original.seek(0)

        compactar(self.arquivo_original.name, self.arquivo_compactado.name)
        descompactar(self.arquivo_compactado.name, self.arquivo_recuperado.name)

        self.arquivo_recuperado.seek(0)
        texto_recuperado = self.arquivo_recuperado.read()

        self.assertEqual(texto_original, texto_recuperado)


if __name__ == '__main__':
    unittest.main()
