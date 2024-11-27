from tokenize import Token
import LerArquivo


class Analisador:
    def __init__(self, arquivo):
        self.fr = LerArquivo(arquivo)
        self.valor = []
        self.tokens = []
        self.tokens_agrupados = []
        self.id_value = ""
        self.num_value = ""
        self.count_line = 1

    def get_lista(self):
        return self.tokens

    def get_tokens_agrupados(self):
        return self.tokens_agrupados

    def agrupa_tokens(self):
        for i, token in enumerate(self.tokens):
            if not token.is_impressed():
                temp = f"{token.valor}\t{token.tipo}\t\t{token.posicao}"
                print(temp, end="")
                for j in range(i + 1, len(self.tokens)):
                    if token.valor == self.tokens[j].valor:
                        print(f", {self.tokens[j].posicao}", end="")
                        temp += f", {self.tokens[j].posicao}"
                        self.tokens[j].set_impressed(True)
                self.tokens_agrupados.append(temp)
                print()

    def outra_forma(self):
        outra_forma = []
        for token in self.tokens:
            if token.tipo in ["num", "id"]:
                outra_forma.append(token.tipo)
            else:
                outra_forma.append(token.valor)
        return " ".join(outra_forma)

    def analisador_lexico(self):
        caractere_lido = -1
        while (caractere_lido := self.fr.read_next_char()) != -1:
            c = chr(caractere_lido)
            if c in [' ', '\n', '\r']:
                self._processar_valores_pendentes()
                if c == '\n':
                    self.count_line += 1
            elif c.isalpha():
                self.id_value += c
            elif c.isdigit():
                self.num_value += c
            elif c == '.':
                self.num_value += c
            else:
                self._processar_valores_pendentes()
                self._processar_operadores(c)

    def _processar_valores_pendentes(self):
        if self.id_value:
            self.tokens.append(Token("id", self.id_value, self.count_line))
            self.id_value = ""
        if self.num_value:
            self.tokens.append(Token("num", self.num_value, self.count_line))
            self.num_value = ""

    def _processar_operadores(self, c):
        operadores = {
            '=': "opIgual",
            '+': "opSoma",
            '-': "opDif",
            '*': "opMult",
            '/': "opDiv",
            ';': "simbEsp",
            '(': "simbEsp",
            ')': "simbEsp",
        }
        if c in operadores:
            self.tokens.append(Token(operadores[c], c, self.count_line))
        else:
            raise RuntimeError(f"Símbolo não reconhecido: {c} na linha {self.count_line}")
