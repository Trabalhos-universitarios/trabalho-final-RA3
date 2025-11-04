
import unittest
from src.frequencias import gerar_tabela_frequencias

class TestFrequencias(unittest.TestCase):

    def test_gerar_tabela_frequencias(self):
        """Testa se a tabela de frequências é gerada corretamente."""
        texto = "banana bandada"
        
        # Dicionário esperado, ordenado alfabeticamente
        esperado = {
            ' ': 1,
            'a': 6,
            'b': 2,
            'd': 2,
            'n': 3
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

