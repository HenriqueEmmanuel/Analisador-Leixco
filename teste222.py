import re

class Analisador:
    def __init__(self, caminho_entrada):
        self.caminho_entrada = caminho_entrada
        self.tokens = []  
        self.tabela_simbolos = {}  
        self.proximo_id = 1  
        self.tokens_com_ids = []  

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

                conteudo_sem_comentarios = re.sub(r"//.*", "", conteudo)
                conteudo_sem_comentarios = re.sub(r"/\*.*?\*/", "", conteudo_sem_comentarios, flags=re.DOTALL)

                print("Conteúdo do arquivo sem comentários:\n")
                print(conteudo_sem_comentarios)  

                padrao = r"[a-zA-Z_][a-zA-Z_0-9]*|\d+\.\d+|\d+|[\{\}\[\]\(\),;=+\-*/\"']"
                self.tokens = re.findall(padrao, conteudo_sem_comentarios)
        except FileNotFoundError:
            print(f"Erro: O arquivo {self.caminho_entrada} não foi encontrado.")
            exit()

    def agrupa_tokens(self):
        resultado = []  

        delimitadores_comum = {"{", "}", "(", ")", "[", "]", ",", ";", "\"", "\'", "."}
        
        for token in self.tokens:
            if token.startswith("\"") and token.endswith("\""):
                simbolo = "STRING"
                token = token[1:-1] 
                token = token.replace("\\\"", "\"").replace("\\n", "\n").replace("\\t", "\t")
                resultado.append((f"\"{token}\"", simbolo))
            elif re.match(r"^\d+(\.\d+)?$", token):
                simbolo = "Número"
                resultado.append((token, simbolo))
            else:
                simbolo = self.palavras_reservadas_java.get(token, "Desconhecido")

                if simbolo == "Desconhecido":  
                    if token in delimitadores_comum:
                        simbolo = "Delimitador"
                        resultado.append((token, simbolo))
                    else:
                        if token == "+":
                            simbolo = "Operador de Soma"
                        elif token == "-":
                            simbolo = "Operador de Subtracao"
                        elif token == "*":
                            simbolo = "Operador de Multiplicacao"
                        elif token == "**":
                            simbolo = "Operador de Potencia"
                        elif token == "/":
                            simbolo = "Operador de Divisao"
                        elif token == "=":
                            simbolo = "Operador de Atribuicao"
                        elif token in {"<", ">", "<=", ">=", "==", "!="}:
                            simbolo = "Operador de Comparacao"
                        elif token in {"&&", "||", "!"}:
                            simbolo = "Operador Logico"
                        elif token in {"&", "|", "^", "~"}:
                            simbolo = "Operador Bitwise"
                        elif token == "%":
                            simbolo = "Operador de Modulo"
                        else:
                            simbolo = None  

                        if simbolo:
                            resultado.append((token, simbolo))
                        else:  
                            if token not in self.tabela_simbolos:
                                self.tabela_simbolos[token] = self.proximo_id
                                self.proximo_id += 1
                            simbolo = "Identificador"
                            id_unico = self.tabela_simbolos[token]
                            resultado.append((f"id,{id_unico}", simbolo))
                else:
                    resultado.append((token, simbolo))

        self.tokens_com_ids = resultado

    def gerar_arquivo_saida(self):
        try:
            caminho_saida = "saida.txt"  
            with open(caminho_saida, "w") as arquivo_saida:
                arquivo_saida.write("Tabela de Símbolos:\n")
                arquivo_saida.write("Identificador         ID\n")
                for simbolo, id_unico in self.tabela_simbolos.items():
                    arquivo_saida.write(f"{simbolo:<20}{id_unico}\n")

                arquivo_saida.write("\n\nLista de Tokens:\n")
                arquivo_saida.write("Token               Tipo            ID\n\n")
                for token, tipo in self.tokens_com_ids:
                    if tipo == "Delimitador" or tipo == "Operador":
                        arquivo_saida.write(f"{token:<15}\t{tipo:<20}\n")
                    else:
                        if token.startswith("id,"):
                            id_ = token.split(",")[1]  
                            arquivo_saida.write(f"{token:<15}\t{tipo:<20}{id_}\n")
                        else:
                            arquivo_saida.write(f"{token:<15}\t{tipo:<20}\n")

            print("Arquivo de saída gerado com sucesso.")
        except Exception as e:
            print(f"Erro ao gerar o arquivo de saída: {e}")

def main():
    caminho_entrada = "teste.txt"  

    anas = Analisador(caminho_entrada)
    anas.analisador_lexico()  
    anas.agrupa_tokens()  
    anas.gerar_arquivo_saida()  

if __name__ == "__main__":
    main()
