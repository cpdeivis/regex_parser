from sly import Parser
from RElex import RegexLexer
from Automata import State

class RegexParser(Parser):
    tokens = RegexLexer.tokens

    def __init__(self):
        self.eAlphabet = set([])
        self.eStates = {}
        State._counter = 0

    @_("union", "simple_re")
    def re(self, p):
        print(p._slice)
        if "union" in p._namemap:
            return p.union
        else:
            return p.simple_re

    @_("re ALT simple_re")
    def union(self, p):
        print(p._slice)
        start = State(False)
        end = State(True)
        f_start, f_end = p.re
        s_start, s_end = p.simple_re

        start.addEpsilonTransition(f_start)
        start.addEpsilonTransition(s_start)

        f_end.isEnd = False
        s_end.isEnd = False
        f_end.addEpsilonTransition(end)
        s_end.addEpsilonTransition(end)

        self.eStates[start.name] = start
        self.eStates[end.name] = end
        return (start, end)

    @_("concatenation", "basic_re")
    def simple_re(self, p):
        print(p._slice)
        if "concatenation" in p._namemap:
            return p.concatenation
        else:
            return p.basic_re

    @_("simple_re basic_re")
    def concatenation(self, p):
        print(p._slice)
        f_start, f_end = p.simple_re
        s_start, s_end = p.basic_re

        f_end.isEnd = False
        f_end.addEpsilonTransition(s_start)

        return (f_start, s_end)
    
    @_("star", "plus", "question", "elementary_re")
    def basic_re(self, p):
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
        print(p._slice)
        start = State(False)
        end = State(True)
        p_start, p_end = p.elementary_re

        p_end.isEnd = False
        start.addEpsilonTransition(end)
        start.addEpsilonTransition(p_start)
        p_end.addEpsilonTransition(end)
        p_end.addEpsilonTransition(p_start)

        self.eStates[start.name] = start
        self.eStates[end.name] = end
        return (start, end)

    @_("elementary_re F_PLUS")
    def plus(self, p):
        print(p._slice)
        end = State(True)
        start, p_end = p.elementary_re

        p_end.isEnd = False
        p_end.addEpsilonTransition(end)
        end.addEpsilonTransition(start)

        self.eStates[end.name] = end
        return (start, end)

    @_("elementary_re QMARK")
    def question(self, p):
        print(p._slice)
        start = State(False)
        end = State(True)
        p_start, p_end = p.elementary_re

        p_end.isEnd = False
        start.addEpsilonTransition(end)
        start.addEpsilonTransition(p_start)
        p_end.addEpsilonTransition(end)

        self.eStates[start.name] = start
        self.eStates[end.name] = end
        return (start, end)

    # @_("group", "ESCAPE", "DOT", "CHAR", "set")
    @_("group", "ESCAPE", "CHAR", "set")
    def elementary_re(self, p):
        print(p._slice)
        symbol =  p.ESCAPE if "ESCAPE" in p._namemap else (p.CHAR if "CHAR" in p._namemap else None)
        if symbol:
            start = State(False)
            end = State(True)
            start.addSymbolTransition(symbol, end)

            self.eAlphabet.add(symbol)
            self.eStates[start.name] = start
            self.eStates[end.name] = end
            return (start, end)

        return p.group if "group" in p._namemap else p.set

    @_("LPAREN re RPAREN")
    def group(self, p):
        print(p._slice)
        return p.re

    @_("LBRACK set_items RBRACK")
    def set(self, p):
        print(p.set_items)
        start = State(False)
        end = State(True)
        for item in p.set_items:
            start.addSymbolTransition(item, end)

        self.eStates[start.name] = start
        self.eStates[end.name] = end
        return (start, end)

    @_("set_items set_item")
    def set_items(self, p):
        print(p._slice)
        p.set_items.append(p.set_item)
        return p.set_items
            
    @_("set_item")
    def set_items(self, p):
        return [ p.set_item ]

    # @_("ESCAPE", "DOT", "CHAR")
    @_("ESCAPE", "CHAR")
    def set_item(self, p):
        print(p._slice)
        symbol = p.CHAR if "CHAR" in p._namemap else p.ESCAPE

        self.eAlphabet.add(symbol)
        return symbol
