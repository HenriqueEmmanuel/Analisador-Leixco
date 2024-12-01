import re

class Analisador:
    def __init__(self, caminho_entrada):
        self.caminho_entrada = caminho_entrada
        self.tokens = []  # Lista de tokens extraídos
        self.tabela_simbolos = {}  # Tabela de símbolos
        self.proximo_id = 1  # Contador para os IDs dos identificadores
        self.tokens_com_ids = []  # Tokens com IDs associados

        # Definindo as palavras reservadas do Java
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

    # Função que realiza a análise léxica
    def analisador_lexico(self):
        try:
            with open(self.caminho_entrada, "r") as arquivo:
                conteudo = arquivo.read()

                # Remover comentários do código
                conteudo_sem_comentarios = re.sub(r"//.*", "", conteudo)
                conteudo_sem_comentarios = re.sub(r"/\*.*?\*/", "", conteudo_sem_comentarios, flags=re.DOTALL)

                # Exibir o conteúdo sem comentários (para verificação)
                print("Conteúdo do arquivo sem comentários:\n")
                print(conteudo_sem_comentarios)

                # Expressão regular para identificar os tokens
                padrao = r"[a-zA-Z_][a-zA-Z_0-9]*|\d+\.\d+|\d+|[\{\}\[\]\(\),;=+\-*/\"'\.\<\>\=\!\&\|\^\~\%\?]"
                self.tokens = re.findall(padrao, conteudo_sem_comentarios)

        except FileNotFoundError:
            print(f"Erro: O arquivo {self.caminho_entrada} não foi encontrado.")
            exit()

    # Função para agrupar os tokens e identificar seus tipos
    def agrupa_tokens(self):
        resultado = []  # Lista para armazenar os tokens agrupados
        delimitadores_comum = {"{", "}", "(", ")", "[", "]", ",", ";", "\"", "\'", "."}

        operadores_comparacao = {"<", ">", "<=", ">=", "==", "!="}  # Definindo operadores de comparação

        for token in self.tokens:
            if token.startswith("\"") and token.endswith("\""):  # Se for uma string
                simbolo = "STRING"
                token = token[1:-1]  # Remover as aspas
                token = token.replace("\\\"", "\"").replace("\\n", "\n").replace("\\t", "\t")  # Destruir escapes
                # Inserir a string como um token único
                resultado.append((f"\"{token}\"", simbolo))
            elif re.match(r"^\d+(\.\d+)?$", token):  # Se for número (inteiro ou flutuante)
                simbolo = "Número"
                resultado.append((token, simbolo))
            else:
                simbolo = self.palavras_reservadas_java.get(token, "Desconhecido")

                if simbolo == "Desconhecido":
                    if token in delimitadores_comum:
                        simbolo = "Delimitador"
                        resultado.append((token, simbolo))
                    elif token in operadores_comparacao:
                        simbolo = "Operador de Comparacao"
                        resultado.append((token, simbolo))
                    else:
                        # Tratando outros operadores aritméticos
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
                        elif token in {"&&", "||", "!"}:
                            simbolo = "Operador Logico"
                        elif token in {"&", "|", "^", "~"}:
                            simbolo = "Operador Bitwise"
                        elif token == "%":
                            simbolo = "Operador de Modulo"
                        else:
                            simbolo = None  # Para identificadores

                        if simbolo:
                            resultado.append((token, simbolo))
                        else:  # Identificador
                            if token not in self.tabela_simbolos:
                                self.tabela_simbolos[token] = self.proximo_id
                                self.proximo_id += 1
                            simbolo = "Identificador"
                            id_unico = self.tabela_simbolos[token]
                            resultado.append((f"id,{id_unico}", simbolo))
                else:
                    resultado.append((token, simbolo))

        self.tokens_com_ids = resultado

    # Função para gerar o arquivo de saída
    def gerar_arquivo_saida(self):
        try:
            caminho_saida = "saida.txt"  # Caminho de saída
            with open(caminho_saida, "w", encoding="utf-8") as arquivo_saida:
                arquivo_saida.write("Tabela de Símbolos:\n")
                arquivo_saida.write("Identificador         ID\n")
                for simbolo, id_unico in self.tabela_simbolos.items():
                    arquivo_saida.write(f"{simbolo:<20}{id_unico}\n")

                arquivo_saida.write("\n\nLista de Tokens:\n")
                arquivo_saida.write("Token               Tipo            ID\n\n")
                for token, tipo in self.tokens_com_ids:
                    if tipo == "Delimitador" or tipo == "Operador":
                        arquivo_saida.write(f"{token:<15}{tipo}\n")
                    else:
                        id_unico = self.tabela_simbolos.get(token, None)
                        arquivo_saida.write(f"{token:<15}{tipo:<20}{id_unico}\n")
        except Exception as e:
            print(f"Erro ao gerar o arquivo de saída: {e}")

# Função principal que orquestra a análise léxica e a geração de saída
def main():
    caminho_entrada = "teste.txt"  # Caminho do arquivo de entrada

    anas = Analisador(caminho_entrada)
    anas.analisador_lexico()  # Realizar a análise léxica
    anas.agrupa_tokens()  # Agrupar os tokens e identificar seus tipos
    anas.gerar_arquivo_saida()  # Gerar o arquivo de saída

# Executar a função principal
if __name__ == "__main__":
    main()
