class LerArquivo:
    def __init__(self, caminho):
        self.caminho = caminho
        self.conteudo = self._carregar_arquivo()
        self.posicao = 0

    def _carregar_arquivo(self):
        with open(self.caminho, 'r') as arquivo:
            return arquivo.read()

    def read_next_char(self):
        if self.posicao >= len(self.conteudo):
            return -1
        char = self.conteudo[self.posicao]
        self.posicao += 1
        return char
