import re

class Analisador:
    def __init__(self, caminho_entrada):
        self.caminho_entrada = caminho_entrada
        self.tokens = []  # Lista de tokens
        self.tabela_simbolos = {}  # Tabela de símbolos (identificadores)
        self.proximo_id = 1  # ID único para cada identificador na tabela de símbolos

        # Dicionário de palavras reservadas Java
        self.palavras_reservadas_java = {
            "abstract": "Palavra-chave",
            "assert": "Palavra-chave",
            "boolean": "Tipo de dado",
            "break": "Palavra-chave",
            "byte": "Tipo de dado",
            "case": "Palavra-chave",
            "catch": "Palavra-chave",
            "char": "Tipo de dado",
            "class": "Palavra-chave",
            "const": "Palavra-chave",
            "continue": "Palavra-chave",
            "default": "Palavra-chave",
            "do": "Palavra-chave",
            "double": "Tipo de dado",
            "else": "Palavra-chave",
            "enum": "Palavra-chave",
            "extends": "Palavra-chave",
            "final": "Palavra-chave",
            "finally": "Palavra-chave",
            "float": "Tipo de dado",
            "for": "Palavra-chave",
            "goto": "Palavra-chave",
            "if": "Palavra-chave",
            "implements": "Palavra-chave",
            "import": "Palavra-chave",
            "instanceof": "Palavra-chave",
            "int": "Tipo de dado",
            "interface": "Palavra-chave",
            "long": "Tipo de dado",
            "native": "Palavra-chave",
            "new": "Palavra-chave",
            "null": "Valor especial",
            "package": "Palavra-chave",
            "private": "Palavra-chave",
            "protected": "Palavra-chave",
            "public": "Palavra-chave",
            "return": "Palavra-chave",
            "short": "Tipo de dado",
            "static": "Palavra-chave",
            "strictfp": "Palavra-chave",
            "super": "Palavra-chave",
            "switch": "Palavra-chave",
            "synchronized": "Palavra-chave",
            "this": "Palavra-chave",
            "throw": "Palavra-chave",
            "throws": "Palavra-chave",
            "transient": "Palavra-chave",
            "try": "Palavra-chave",
            "void": "Tipo de dado",
            "volatile": "Palavra-chave",
            "while": "Palavra-chave"
        }

    def analisador_lexico(self):
        try:
            with open(self.caminho_entrada, "r") as arquivo:
                conteudo = arquivo.read()
                print("Conteúdo do arquivo lido:")
                print(conteudo)  

                padrao = r"[a-zA-Z_][a-zA-Z_0-9]*|[\{\}\[\]\(\),;=+*/\"'\.]"  # Incluindo ponto (.)
                self.tokens = re.findall(padrao, conteudo)
        except FileNotFoundError:
            print(f"Erro: O arquivo {self.caminho_entrada} não foi encontrado.")
            exit()

    def agrupa_tokens(self):
        resultado = []  # Lista para armazenar os tokens com seus tipos e IDs

        delimitadores_comum = {"{", "}", "(", ")", "[", "]", ",", ";", "\"", "\'", ".", " "}

        for token in self.tokens:
            simbolo = self.palavras_reservadas_java.get(token, "Desconhecido")

            if simbolo == "Desconhecido":  # Se o token não for uma palavra reservada
                # Verifica se o token já está na tabela de símbolos
                if token not in self.tabela_simbolos and token not in delimitadores_comum:
                    # Adiciona o identificador à tabela de símbolos com um ID único
                    self.tabela_simbolos[token] = f"id,{self.proximo_id}"
                    self.proximo_id += 1
                # Atribui o ID do identificador na tabela de símbolos
                simbolo = "Identificador"
                # Recupera o ID único do identificador
                id_unico = self.tabela_simbolos.get(token, None)
                # Adiciona o token com o formato "id,<id>" na lista de tokens
                if id_unico:
                    resultado.append((id_unico, simbolo))
            else:
                # Palavras reservadas, adiciona diretamente à lista de tokens
                resultado.append((token, simbolo))

            # Se for um delimitador comum, marca como "Delimitador"
            if token in delimitadores_comum:
                simbolo = "Delimitador"
                # Não adiciona ID para delimitadores
                resultado.append((token, simbolo))

        return resultado

def main():
    caminho_entrada = "teste.txt"

    anas = Analisador(caminho_entrada)
    anas.analisador_lexico()  
    tokens_com_ids = anas.agrupa_tokens()  

    # Exibe a tabela de símbolos com seus identificadores
    print("\nTabela de Símbolos (Identificadores com ID):")
    for identificador, id_ in anas.tabela_simbolos.items():
        print(f"Identificador: {identificador} -> {id_}")

    print("\nTokens com IDs únicos:")
    print("Token           Tipo                       Tabela de Símbolo                 ID\n")
    for token, simbolo in tokens_com_ids:
        print(f"{token:<15}\t{simbolo:<25}")

if __name__ == "__main__":
    main()
