from collections import deque, defaultdict
from typing import Dict, List


class MaxFlow:
    def __init__(self, vertices: int):
        """
        Инициализация графа с заданным количеством вершин.

        Args:
            vertices: количество вершин
        """
        self.V = vertices
        # graph[u][v] = пропускная способность ребра u→v
        self.graph: Dict[int, Dict[int, int]] = defaultdict(
            lambda: defaultdict(int)
        )

    def add_edge(self, u: int, v: int, capacity: int) -> None:
        """
        Добавить ориентированное ребро в граф.

        Args:
            u: исходная вершина
            v: целевая вершина
            capacity: пропускная способность
        """
        self.graph[u][v] += capacity  # поддержка множественных рёбер

    def _bfs(self, s: int, t: int, parent: List[int]) -> bool:
        """
        Поиск в ширину (BFS) по остаточному графу.
        Используется для проверки наличия пути от s к t.

        Args:
            s: исходная вершина (источник)
            t: целевая вершина (сток)
            parent: массив для хранения предков (для восстановления пути)

        Returns:
            True, если путь найден; иначе False
        """
        visited = [False] * self.V
        queue = deque([s])
        visited[s] = True
        parent[s] = -1

        # S3: BFS основной цикл
        while queue:
            u = queue.popleft()

            # Проходим по всем соседям u в остаточном графе
            for v, cap in self.graph[u].items():
                # Если вершина не посещена и есть остаточная пропускная способность
                if not visited[v] and cap > 0:
                    queue.append(v)
                    parent[v] = u
                    visited[v] = True

                    # Если достигли стока, путь найден
                    if v == t:
                        return True

        return False

    def ford_fulkerson(self, s: int, t: int) -> int:
        """
        Найти максимальный поток от источника s к стоку t.

        Использует алгоритм Ford–Fulkerson с BFS (Edmonds–Karp).

        Args:
            s: источник
            t: сток

        Returns:
            Максимальное значение потока от s к t

        Временная сложность: O(V * E^2) в худшем случае
        """
        # S1: Инициализация
        parent = [-1] * self.V
        max_flow = 0

        # S2-S6: Основной цикл — пока существуют дополняющие пути
        while self._bfs(s, t, parent):

            # S4: Находим минимальную пропускную способность на пути
            # (узкое место)
            path_flow = float("inf")
            v = t
            while v != s:
                u = parent[v]
                path_flow = min(path_flow, self.graph[u][v])
                v = u

            # S5: Обновляем остаточные пропускные способности рёбер
            # (как в прямом, так и в обратном направлении)
            v = t
            while v != s:
                u = parent[v]
                # Уменьшаем пропускную способность в прямом направлении
                self.graph[u][v] -= path_flow
                # Увеличиваем в обратном направлении (для поддержки отмены)
                self.graph[v][u] += path_flow
                v = u

            # S6: Добавляем найденный поток к общему потоку
            max_flow += path_flow

        # S7: Возвращаем максимальный поток
        return int(max_flow)


# ===== ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ =====

if __name__ == "__main__":
    print("=" * 50)
    print("Пример: Максимальный поток в сети")
    print("=" * 50)

    # Создаём граф с 6 вершинами (0-5)
    g = MaxFlow(6)

    # Добавляем рёбра (u, v, capacity)
    g.add_edge(0, 1, 16)
    g.add_edge(0, 2, 13)
    g.add_edge(1, 2, 10)
    g.add_edge(1, 3, 12)
    g.add_edge(2, 1, 4)
    g.add_edge(2, 4, 14)
    g.add_edge(3, 2, 9)
    g.add_edge(3, 5, 20)
    g.add_edge(4, 3, 7)
    g.add_edge(4, 5, 4)

    print("\nГраф (пропускные способности):")
    print("0 → 1: 16")
    print("0 → 2: 13")
    print("1 → 2: 10")
    print("1 → 3: 12")
    print("2 → 1: 4")
    print("2 → 4: 14")
    print("3 → 2: 9")
    print("3 → 5: 20")
    print("4 → 3: 7")
    print("4 → 5: 4")

    source = 0
    sink = 5

    # Находим максимальный поток
    max_flow_value = g.ford_fulkerson(source, sink)

    print(f"\nИсточник (s): {source}")
    print(f"Сток (t): {sink}")
    print(f"\nМаксимальный поток = {max_flow_value}")

    # Пример 2: Простой граф
    print("\n" + "=" * 50)
    print("Пример 2: Простая сеть (3 вершины)")
    print("=" * 50)

    g2 = MaxFlow(3)
    g2.add_edge(0, 1, 1000)
    g2.add_edge(0, 2, 1000)
    g2.add_edge(1, 2, 1)

    print("\nГраф:")
    print("0 → 1: 1000")
    print("0 → 2: 1000")
    print("1 → 2: 1")

    max_flow_value2 = g2.ford_fulkerson(0, 2)
    print(f"\nМаксимальный поток от 0 к 2 = {max_flow_value2}")
