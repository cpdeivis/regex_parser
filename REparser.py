from sly import Parser
from RElex import RegexLexer


class RegexParser(Parser):
    tokens = RegexLexer.tokens
    debugfile = 'parser.out'

    @_("union", "simple_re")
    def re(self, p):
        pass

    @_("re ALT simple_re")
    def union(self, p):
        pass

    @_("concatenation", "basic_re")
    def simple_re(self, p):
        pass

    @_("simple_re basic_re")
    def concatenation(self, p):
        pass
    
    @_("star", "plus", "elementary_re")
    def basic_re(self, p):
        pass

    @_("elementary_re F_STAR")
    def star(self, p):
        pass

    @_("elementary_re F_PLUS")
    def plus(self, p):
        pass

    @_("group", "ESCAPE", "DOT", "CHAR", "set")
    def elementary_re(self, p):
        pass
    
    @_("LPAREN re RPAREN")
    def group(self, p):
        pass

    @_("LBRACK set_items RBRACK")
    def set(self, p):
        pass

    @_("set_item", "set_item set_items")
    def set_items(self, p):
        pass

    @_("ESCAPE", "DOT", "CHAR")
    def set_item(self, p):
        pass
