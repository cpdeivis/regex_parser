# Interpretador para Expressões Regulares

O objetivo deste trabalho é a criação de uma GLC para a representação de Expressões Regulares e a implementação de um interpretador para estas expressões, permitindo o reconhecimento (ou não) de palavras de acordo com sua especificação.

**Disciplina**: ELC 408 – Compiladores.

**Professor**: Giovani Rubert Librelotto.

**Grupo**: 
- Claiton Neisse;
- Deivis Costa Pereira;
- William Felipe de Almeida.

## Implementação
A Gramática utilizada é descrita abaixo, também é especificada nos decoradores dos métodos da classe RegexParser.
```
re: union 
  | simple_re

union:  re ALT simple_re

simple_re:  concatenation 
         |  basic_re

concatenation: simple_re basic_re

basic_re:   star
        |   plus
        |   question
        |   elementary_re

star:  elementary_re F_STAR

plus:  elementary_re F_PLUS

question:  elementary_re QMARK

elementary_re:  group
             |  set
             |  ESCAPE
             |  CHAR

group:  LPAREN re RPAREN

set:  LBRACK set_items RBRACK

set_items:  set_items set_item
         |  set_item

set_item:  ESCAPE
        |  CHAR
```

O método de construção utilizado é o Algoritmo de Thompson, tranforma a expressão regular de entrada em um autômato finito não determinístico com movimentos epsilon.

O parser foi implementado utilizando o gerador de parser [SLY(Sly Lex Yacc)](https://sly.readthedocs.io/en/latest/).

## Execução
É necessário possuir o python > 3.7 instalado na máquina juntamente com as dependências elencadas em requirements.txt.

```bash
# instalação das dependências utilizando o pip
pip install -r requirements.txt
```

Para utilizar o programa é necessário executar o arquivo main.py. O mesmo irá fornecer um prompt para inserção da expressão regular desejada. Caso a ER seja válida um novo prompt será fornecido para inserção de strings de teste.
```bash
python main.py
```