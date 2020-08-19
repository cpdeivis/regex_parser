from sly import Parser
from RElex import RegexLexer
from Automata import eNFA


class RegexParser(Parser):
    # Obtem lista de tokens do lexer
    tokens = RegexLexer.tokens

    def __init__(self, isVerbose=False):
        self.Automaton = eNFA()
        self.Verbose = isVerbose

    # Regras gramaticais e ações
    # Os argumentos dos decoradores são o lado direito das regras da gramatica
    @_("union", "simple_re")
    def re(self, p):
        if self.Verbose:
            print(p._slice)
        if "union" in p._namemap:
            self.Automaton.Start = p.union[0]
            return p.union
        else:
            self.Automaton.Start = p.simple_re[0]
            return p.simple_re

    @_("re ALT simple_re")
    def union(self, p):
        if self.Verbose:
            print(p._slice)
        start = self.Automaton.createState(False)
        end = self.Automaton.createState(True)
        f_start, f_end = p.re
        s_start, s_end = p.simple_re

        self.Automaton.addEpsilonTransition(start, f_start)
        self.Automaton.addEpsilonTransition(start, s_start)

        self.Automaton.End.remove(f_end)
        self.Automaton.End.remove(s_end)
        self.Automaton.addEpsilonTransition(f_end, end)
        self.Automaton.addEpsilonTransition(s_end, end)

        return (start, end)

    @_("concatenation", "basic_re")
    def simple_re(self, p):
        if self.Verbose:
            print(p._slice)
        if "concatenation" in p._namemap:
            return p.concatenation
        else:
            return p.basic_re

    @_("simple_re basic_re")
    def concatenation(self, p):
        if self.Verbose:
            print(p._slice)
        f_start, f_end = p.simple_re
        s_start, s_end = p.basic_re

        self.Automaton.End.remove(f_end)
        self.Automaton.addEpsilonTransition(f_end, s_start)

        return (f_start, s_end)

    @_("star", "plus", "question", "elementary_re")
    def basic_re(self, p):
        if self.Verbose:
            print(p._slice)
        if "star" in p._namemap:
            return p.star
        elif "plus" in p._namemap:
            return p.plus
        elif "question" in p._namemap:
            return p.question
        else:
            return p.elementary_re

    @_("elementary_re F_STAR")
    def star(self, p):
        if self.Verbose:
            print(p._slice)
        start = self.Automaton.createState(False)
        end = self.Automaton.createState(True)
        p_start, p_end = p.elementary_re

        self.Automaton.End.remove(p_end)
        self.Automaton.addEpsilonTransition(start, end)
        self.Automaton.addEpsilonTransition(start, p_start)
        self.Automaton.addEpsilonTransition(p_end, end)
        self.Automaton.addEpsilonTransition(p_end, p_start)

        return (start, end)

    @_("elementary_re F_PLUS")
    def plus(self, p):
        if self.Verbose:
            print(p._slice)
        end = self.Automaton.createState(True)
        start, p_end = p.elementary_re

        self.Automaton.End.remove(p_end)
        self.Automaton.addEpsilonTransition(p_end, end)
        self.Automaton.addEpsilonTransition(end, start)

        return (start, end)

    @_("elementary_re QMARK")
    def question(self, p):
        if self.Verbose:
            print(p._slice)
        start = self.Automaton.createState(False)
        end = self.Automaton.createState(True)
        p_start, p_end = p.elementary_re

        self.Automaton.End.remove(p_end)
        self.Automaton.addEpsilonTransition(start, end)
        self.Automaton.addEpsilonTransition(start, p_start)
        self.Automaton.addEpsilonTransition(p_end, end)

        return (start, end)

    # @_("group", "ESCAPE", "DOT", "CHAR", "set")
    @_("group", "ESCAPE", "CHAR", "set")
    def elementary_re(self, p):
        if self.Verbose:
            print(p._slice)
        symbol = (
            p.ESCAPE
            if "ESCAPE" in p._namemap
            else (p.CHAR if "CHAR" in p._namemap else None)
        )
        if symbol:
            start = self.Automaton.createState(False)
            end = self.Automaton.createState(True)
            self.Automaton.addSymbolTransition(symbol, start, end)

            return (start, end)

        return p.group if "group" in p._namemap else p.set

    @_("LPAREN re RPAREN")
    def group(self, p):
        if self.Verbose:
            print(p._slice)
        return p.re

    @_("LBRACK set_items RBRACK")
    def set(self, p):
        if self.Verbose:
            print(p.set_items)
        start = self.Automaton.createState(False)
        end = self.Automaton.createState(True)
        for item in p.set_items:
            self.Automaton.addSymbolTransition(item, start, end)

        return (start, end)

    @_("set_items set_item")
    def set_items(self, p):
        if self.Verbose:
            print(p._slice)
        p.set_items.append(p.set_item)
        return p.set_items

    @_("set_item")
    def set_items(self, p):
        return [p.set_item]

    # @_("ESCAPE", "DOT", "CHAR")
    @_("ESCAPE", "CHAR")
    def set_item(self, p):
        if self.Verbose:
            print(p._slice)
        symbol = p.CHAR if "CHAR" in p._namemap else p.ESCAPE

        return symbol

    def error(self, token):
        if token:
            lineno = getattr(token, "lineno", 0)
            if lineno:
                print(f"Erro de sintaxe na linha {lineno}, token={token.type}!")
            else:
                print(f"Erro de sintaxe, token={token.type}!")
        else:
            print("Erro ao parsear a entrada. EOF\n")

        raise KeyError()
