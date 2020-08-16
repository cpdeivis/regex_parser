from sly import Lexer


class RegexLexer(Lexer):
    tokens = {
        ESCAPE,
        LBRACK,
        RBRACK,
        LPAREN,
        RPAREN,
        F_STAR,
        F_PLUS,
        QMARK,
        ALT,
        CHAR,
    }
    @_(r"\\.")
    def ESCAPE(self, t):
        t.value = t.value[-1]
        return t
    
    LBRACK = r"\["
    RBRACK = r"\]"
    LPAREN = r"\("
    RPAREN = r"\)"
    F_STAR = r"\*"
    F_PLUS = r"\+"
    QMARK = r"\?"
    # DOT = r"\."
    ALT = r"\|"
    CHAR = r"."