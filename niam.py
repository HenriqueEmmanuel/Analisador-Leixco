import re

class Analisador:
    def __init__(self, caminho_entrada):
        self.caminho_entrada = caminho_entrada
        self.tokens = []  
        self.mapeamento_ids = {}  
        self.proximo_id = 1  

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

                padrao = r"[a-zA-Z_][a-zA-Z_0-9]*|[\{\}\[\]\(\),;=+*/\"']"
                self.tokens = re.findall(padrao, conteudo)
        except FileNotFoundError:
            print(f"Erro: O arquivo {self.caminho_entrada} não foi encontrado.")
            exit()

    def agrupa_tokens(self):
        resultado = []  

        delimitadores_comum = {"{", "}", "(", ")", "[", "]", ",", ";", "\"", "\'", "."}
        
        id_delimitador_comum = None

        for token in self.tokens:
            if token not in self.mapeamento_ids:
                if token in delimitadores_comum:
                    if id_delimitador_comum is None:
                        id_delimitador_comum = self.proximo_id
                        self.proximo_id += 1
                    self.mapeamento_ids[token] = id_delimitador_comum
                else:
                    self.mapeamento_ids[token] = self.proximo_id
                    self.proximo_id += 1

            id_unico = self.mapeamento_ids[token]

            simbolo = self.palavras_reservadas_java.get(token, "Desconhecido")

            if simbolo == "Desconhecido":
                mapa_simbolos = {
                    "{": "Delimitador",
                    "}": "Delimitador",
                    "(": "Delimitador",
                    ")": "Delimitador",
                    "[": "Delimitador",
                    "]": "Delimitador",
                    ",": "Delimitador",
                    ";": "Delimitador",
                    "\"": "Delimitador",  # aspas duplas
                    "\'": "Delimitador",  # aspas simples
                    ".": "Delimitador",
                    "+": "Operador Aritmético",
                    "=": "Operador de Atribuição",
                    "System.out.println": "Função",
                }
                simbolo = mapa_simbolos.get(token, "Identificador")

            resultado.append((token, simbolo, id_unico))

        return resultado

def main():
    caminho_entrada = "teste.txt"

    anas = Analisador(caminho_entrada)
    anas.analisador_lexico()  
    tokens_com_ids = anas.agrupa_tokens()  

    print("\nTokens com IDs únicos:")
    print("Token           Tipo           Símbolo                 ID\n")
    for token, simbolo, id_ in tokens_com_ids:
        print(f"{token:<15}\t{simbolo:<25}\t{id_}")

if __name__ == "__main__":
    main()
