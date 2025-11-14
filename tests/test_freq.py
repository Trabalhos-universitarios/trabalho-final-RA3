
import unittest
from src.frequencias import gerar_tabela_frequencias

class TestFrequencias(unittest.TestCase):

    def test_gerar_tabela_frequencias(self):
        """Testa se a tabela de frequências é gerada corretamente."""
        texto = "banana bandada"
        
        # O resultado é um Counter, que se comporta como um dicionário.
        # A ordem dos itens não importa para a validação do teste.
        esperado = {
            'a': 6,
            'n': 3,
            'b': 2,
            'd': 2,
            ' ': 1
        }
        
        resultado = gerar_tabela_frequencias(texto)
        self.assertEqual(resultado, esperado)

    def test_string_vazia(self):
        """Testa o comportamento com uma string vazia."""
        texto = ""
        esperado = {}
        resultado = gerar_tabela_frequencias(texto)
        self.assertEqual(resultado, esperado)

if __name__ == '__main__':
    unittest.main()

