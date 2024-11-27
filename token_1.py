class Token:
    def __init__(self, tipo, valor, posicao):
        self.tipo = tipo
        self.valor = valor
        self.posicao = posicao
        self.impressed = False

    def set_impressed(self, value):
        self.impressed = value

    def is_impressed(self):
        return self.impressed

    def __repr__(self):
        return f"Token(tipo={self.tipo}, valor={self.valor}, posicao={self.posicao})"
