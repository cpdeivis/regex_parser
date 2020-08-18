from REparser import RegexLexer, RegexParser
from Automata import DFA, eNFA


if __name__ == "__main__":
    lexer = RegexLexer()
    parser = RegexParser()
    while True:
        try:
            regex = input("\nRegex > ")
            if regex:
                print("Validação da ER")
                parser.parse(lexer.tokenize(regex))
                dfa = DFA()
                dfa.fromNFA(parser.Automaton)
                print("ER Válida")

                while True:
                    try:
                        dfa(input("\nTeste > "))
                    except EOFError:
                        break
                    except ValueError as e:
                        print("ERRO: %s" % str(e))
                        continue
                
                parser.Automaton = eNFA()
        except EOFError:
            break
        except KeyError:
            print("Regex inválida!")
            continue
