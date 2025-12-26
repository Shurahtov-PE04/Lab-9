from typing import Dict, Set, Tuple, Optional


class DFA:
    """
    Класс для реализации детерминированного конечного автомата.

    Атрибуты:
        states: множество всех состояний
        alphabet: алфавит (множество допустимых символов)
        transition: словарь функции переходов (state, char) → next_state
        start_state: начальное состояние
        accept_states: множество принимающих состояний
    """

    def __init__(
            self,
            states: Set[str],
            alphabet: Set[str],
            transition: Dict[Tuple[str, str], str],
            start_state: str,
            accept_states: Set[str],
    ):
        self.states = states
        self.alphabet = alphabet
        self.transition = transition
        self.start_state = start_state
        self.accept_states = accept_states

    def accepts(self, s: str) -> bool:
        """
        Проверка, принимает ли DFA строку s.

        Args:
            s: входная строка

        Returns:
            True, если строка принимается, иначе False
        """
        current = self.start_state

        # S1-S5: Проходим по каждому символу
        for ch in s:
            # Проверяем, принадлежит ли символ алфавиту
            if ch not in self.alphabet:
                return False

            # S4: Выполняем переход
            current = self.transition.get((current, ch))

            # Если переход не определён, строка отклоняется
            if current is None:
                return False

        # S6: Проверяем, достигли ли мы принимающего состояния
        return current in self.accept_states


class SimpleNFA:
    """
    Класс для реализации недетерминированного конечного автомата.
    Поддерживает ε-переходы (epsilon-переходы).
    """

    def __init__(self):
        self.states: Set[int] = set()
        self.start_state: Optional[int] = None
        self.accept_states: Set[int] = set()
        # transitions[state][symbol] = set(next_states)
        self.transitions: Dict[int, Dict[Optional[str], Set[int]]] = {}

    def add_state(self, state: int, is_start=False, is_accept=False):
        """Добавить состояние в автомат."""
        self.states.add(state)
        if is_start:
            self.start_state = state
        if is_accept:
            self.accept_states.add(state)
        if state not in self.transitions:
            self.transitions[state] = {}

    def add_transition(self, from_state: int, symbol: Optional[str], to_state: int):
        """Добавить переход (symbol=None означает ε-переход)."""
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        if symbol not in self.transitions[from_state]:
            self.transitions[from_state][symbol] = set()
        self.transitions[from_state][symbol].add(to_state)

    def _epsilon_closure(self, states: Set[int]) -> Set[int]:
        """Вычислить ε-замыкание множества состояний."""
        stack = list(states)
        closure = set(states)

        while stack:
            state = stack.pop()
            # Ищем все ε-переходы из текущего состояния
            for nxt in self.transitions.get(state, {}).get(None, set()):
                if nxt not in closure:
                    closuare.add(nxt)
                    stack.append(nxt)

        return closure

    def accepts(self, s: str) -> bool:
        """
        Проверка, принимает ли NFA строку s.

        Args:
            s: входная строка

        Returns:
            True, если строка принимается, иначе False
        """
        if self.start_state is None:
            return False

        # Начинаем с ε-замыкания начального состояния
        current_states = self._epsilon_closure({self.start_state})

        # Проходим по каждому символу входной строки
        for ch in s:
            next_states = set()

            # Для каждого текущего состояния вычисляем переходы
            for st in current_states:
                for nxt in self.transitions.get(st, {}).get(ch, set()):
                    next_states.add(nxt)

            # Вычисляем ε-замыкание новых состояний
            current_states = self._epsilon_closure(next_states)

            # Если нет текущих состояний, строка отклоняется
            if not current_states:
                return False

        # Проверяем, есть ли хотя бы одно принимающее состояние
        return any(st in self.accept_states for st in current_states)


import re


def regex_match(pattern: str, s: str) -> bool:
    """
    Проверка строки s на соответствие регулярному выражению pattern.

    Args:
        pattern: регулярное выражение
        s: входная строка

    Returns:
        True, если строка соответствует шаблону, иначе False
    """
    return re.fullmatch(pattern, s) is not None


# ===== ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ =====

# Пример 1: DFA для языка строк, заканчивающихся на "ab"
states = {"q0", "q1", "q2"}
alphabet = {"a", "b"}
transition = {
    ("q0", "a"): "q1",
    ("q0", "b"): "q0",
    ("q1", "a"): "q1",
    ("q1", "b"): "q2",
    ("q2", "a"): "q1",
    ("q2", "b"): "q0",
}
start_state = "q0"
accept_states = {"q2"}

dfa = DFA(states, alphabet, transition, start_state, accept_states)

print("=== DFA Тесты ===")
print(f"dfa.accepts('ab')    = {dfa.accepts('ab')}")  # True
print(f"dfa.accepts('aab')   = {dfa.accepts('aab')}")  # True
print(f"dfa.accepts('aba')   = {dfa.accepts('aba')}")  # False
print(f"dfa.accepts('bbbab') = {dfa.accepts('bbbab')}")  # True

# Пример 2: NFA с ε-переходами
nfa = SimpleNFA()
nfa.add_state(0, is_start=True)
nfa.add_state(1)
nfa.add_state(2, is_accept=True)

nfa.add_transition(0, "a", 1)
nfa.add_transition(1, "b", 2)
nfa.add_transition(0, "b", 0)
nfa.add_transition(1, "a", 1)
nfa.add_transition(2, "a", 2)
nfa.add_transition(2, "b", 2)

print("\n=== NFA Тесты ===")
print(f"nfa.accepts('ab')    = {nfa.accepts('ab')}")  # True
print(f"nfa.accepts('aab')   = {nfa.accepts('aab')}")  # True
print(f"nfa.accepts('ba')    = {nfa.accepts('ba')}")  # False

# Пример 3: Регулярные выражения
email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

print("\n=== Regex Тесты ===")
print(
    f"regex_match(email_pattern, 'example@example.com') = {regex_match(email_pattern, 'example@example.com')}")  # True
print(f"regex_match(email_pattern, 'bad-email') = {regex_match(email_pattern, 'bad-email')}")  # False
