from sly import Lexer


class RegexLexer(Lexer):
    tokens = {
        ESCAPE,
        LBRACE,
        RBRACE,
        LBRACK,
        RBRACK,
        LPAREN,
        RPAREN,
        F_STAR,
        F_PLUS,
        QMARK,
        DOT,
        CHAR,
    }
    ESCAPE = r"\\."
    LBRACE = r"\{"
    RBRACE = r"\}"
    LBRACK = r"\["
    RBRACK = r"\]"
    LPAREN = r"\("
    RPAREN = r"\)"
    F_STAR = r"\*"
    F_PLUS = r"\+"
    QMARK = r"\?"
    DOT = r"\."
    ALT = r"\|"
    CHAR = r"."
