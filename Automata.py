from typing import Dict, Set, List


class State(object):
    _counter: int = 0

    def __init__(self, isEnd):
        self.name: str = "q%s" % State._counter
        self.isEnd: bool = isEnd
        self.sTransitions= {}
        self.eTransitions = []

        State._counter += 1

    def addSymbolTransition(self, symbol, to):
        self.sTransitions[symbol] = to

    def addEpsilonTransition(self, to):
        self.eTransitions.append(to)


def eClosure(state, states):
    state = states[state]
    closures = set([x.name for x in state.eTransitions])
    closures.add(state.name)
    for st in state.eTransitions:
        closures.update(eClosure(st.name, states))
    return closures


def movesNFA(state, states, move):
    moves = set([])
    for st in state:
        if move in states[st].sTransitions:
            moves.add(states[st].sTransitions[move].name)

    return moves


def NFA2DFA(start, end, alpha, states):
    DFA = {}
    counter = 0
    DFA["q" + str(counter)] = {
        "unMark": True,
        "set": eClosure(start.name, states),
        "transitions": {},
        "final": False
    }

    while any([x["unMark"] for x in DFA.values()]):
        atual = next(x for x in DFA.values() if x["unMark"])
        atual["unMark"] = False
        for a in alpha:
            S = set()
            for m in movesNFA(atual["set"], states, a):
                S.update(eClosure(m, states))

            if S:
                if S not in [x["set"] for x in DFA.values()]:
                    counter += 1
                    DFA["q" + str(counter)] = {
                        "unMark": True,
                        "set": S,
                        "transitions": {},
                        "final": False
                    }

                atual["transitions"][a] = next(
                    k for k, v in DFA.items() if v["set"] == S
                )

    for x in [v for v in DFA.values() if (end.name in v["set"])]:
        x["final"] = True

    return DFA