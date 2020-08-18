from __future__ import annotations
from typing import Dict, Set, List


class eState:
    def __init__(self, name):
        self.Name: str = name
        self.Transitions: Dict[str, Set[str]] = {}
        self.Transitions["EPSILON"] = set()

    def addTransition(self, symbol: str, to: str):
        if symbol not in self.Transitions:
            self.Transitions[symbol] = set()
        self.Transitions[symbol].add(to)


class dState:
    def __init__(self, name, S: Set[str]):
        self.Name: str = name
        self.Transitions: Dict[str, Set[str]] = {}
        self._Visited = False
        self._SetNFA: Set[str] = set()
        self._SetNFA.update(S)

    def addTransition(self, symbol: str, to: str):
        self.Transitions[symbol] = to


class eNFA:
    def __init__(self):
        self.Alphabet: Set[str] = set()
        self.States: Dict[str, eState] = {}
        self.Start: str = ""
        self.End: Set[str] = set()

    def _StateName(self) -> str:
        return "q" + str(len(self.States))

    def createState(self, isFinal: bool) -> str:
        name = self._StateName()
        self.States[name] = eState(name)
        if isFinal:
            self.End.add(name)

        return name

    def addSymbolTransition(self, symbol: str, origin: str, to: str):
        self.Alphabet.add(symbol)
        self.States[origin].addTransition(symbol, to)

    def addEpsilonTransition(self, origin: str, to: str):
        self.States[origin].addTransition("EPSILON", to)

    def eClosure(self, state: str) -> Set[str]:
        state = self.States[state]
        closures = set([state.Name])
        closures.update(state.Transitions["EPSILON"])
        # closures.add(state.Name)
        for st in state.Transitions["EPSILON"]:
            closures.update(self.eClosure(st))

        return closures

    def moves(self, states: Set[str], symbol: str) -> Set[str]:
        moves = set()
        for st in states:
            if symbol in self.States[st].Transitions:
                moves.update(self.States[st].Transitions[symbol])

        return moves


class DFA(object):
    def __init__(self):
        self.Alphabet: Set[str] = set()
        self.States: Dict[str, dState] = {}
        self.Start: str = ""
        self.End: Set[str] = set()

    def _StateName(self) -> str:
        return "q" + str(len(self.States))

    def fromNFA(self, nfa: eNFA):
        self.Alphabet = nfa.Alphabet
        self.Start = q0 = self._StateName()
        self.States[q0] = dState(q0, nfa.eClosure(nfa.Start))

        while any(not st._Visited for st in self.States.values()):
            atual: dState = next(st for st in self.States.values() if not st._Visited)
            atual._Visited = True
            for symbol in self.Alphabet:
                S = set()
                for move in nfa.moves(atual._SetNFA, symbol):
                    S.update(nfa.eClosure(move))

                if S:
                    if S not in [st._SetNFA for st in self.States.values()]:
                        qN = self._StateName()
                        self.States[qN] = dState(qN, S)

                    atual.addTransition(
                        symbol,
                        next(k for k, v in self.States.items() if v._SetNFA == S),
                    )

        self.End.update(
            set([k for k, v in self.States.items() if bool(nfa.End & v._SetNFA)])
        )

    def __call__(self, tape: str):
        state = self.Start
        for token in tape:
            if token not in self.Alphabet:
                raise ValueError("O token '%s' não faz parte do alfabeto!" % token)

            if token not in self.States[state].Transitions:
                raise ValueError(
                    "O estado '{0}' não possuí transição com o token '{1}'!".format(
                        state, token
                    )
                )
            aux = self.States[state].Transitions[token]
            print("{0} ---'{1}'---> {2}".format(state, token, aux))
            state = aux

        if state not in self.End:
            raise ValueError(
                "A entrada '%s' não faz parte da linguagem especificada!" % tape
            )

        print("Entrada reconhecida!")
