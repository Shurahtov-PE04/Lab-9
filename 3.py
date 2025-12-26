from typing import List, Tuple
import math

Point = Tuple[float, float]


def orientation(p: Point, q: Point, r: Point) -> int:
    """
    Определить ориентацию упорядоченной тройки точек (p, q, r).

    Args:
        p, q, r: три точки

    Returns:
        0 — точки коллинеарны (лежат на одной линии)
        1 — поворот по часовой стрелке (clockwise)
        2 — поворот против часовой стрелки (counterclockwise)

    Использует кросс-произведение для определения направления поворота:
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

    if abs(val) < 1e-9:  # близко к нулю
        return 0  # коллинеарны

    return 1 if val > 0 else 2  # 1 = clockwise, 2 = counterclockwise


def polar_angle(p0: Point, p: Point) -> float:
    """
    Вычислить полярный угол точки p относительно опорной точки p0.

    Args:
        p0: опорная точка
        p: точка, для которой вычисляется угол

    Returns:
        Угол в радианах (в диапазоне -π до π)
    """
    return math.atan2(p[1] - p0[1], p[0] - p0[0])


def distance_squared(p0: Point, p: Point) -> float:
    """Вычислить квадрат расстояния между двумя точками."""
    return (p[0] - p0[0]) ** 2 + (p[1] - p0[1]) ** 2


def graham_scan(points: List[Point]) -> List[Point]:
    """
    Построить выпуклую оболочку множества точек методом Грэхема.

    Args:
        points: список точек (x, y)

    Returns:
        Список точек выпуклой оболочки в порядке обхода против часовой стрелки

    Временная сложность: O(n log n) из-за сортировки
    Пространственная сложность: O(n)
    """
    n = len(points)

    # S1: Обработка граничных случаев
    if n <= 2:
        return points[:]

    # S2: Находим точку с минимальной y-координатой (опорная точка p0)
    # При равенстве y выбираем точку с минимальной x
    min_idx = 0
    for i in range(1, n):
        if (points[i][1] < points[min_idx][1]) or (
                points[i][1] == points[min_idx][1] and points[i][0] < points[min_idx][0]
        ):
            min_idx = i

    p0 = points[min_idx]

    # S3: Переместим p0 в начало списка (обмен)
    points = [p0] + [points[i] for i in range(n) if i != min_idx]

    # S4: Сортируем остальные точки по полярному углу
    # При равных углах сортируем по расстоянию от p0
    sorted_points = points[1:]
    sorted_points.sort(
        key=lambda p: (polar_angle(p0, p), distance_squared(p0, p))
    )

    # S5: Инициализируем стек (выпуклую оболочку) первыми тремя точками
    hull = [p0, sorted_points[0], sorted_points[1]]

    # S6-S9: Проходим по остальным точкам
    for i in range(2, len(sorted_points)):
        p = sorted_points[i]

        # S8: Удаляем точки, которые создают правый поворот
        while len(hull) >= 2 and orientation(hull[-2], hull[-1], p) != 2:
            hull.pop()

        # S9: Добавляем текущую точку
        hull.append(p)

    # S10: Возвращаем выпуклую оболочку
    return hull


# ===== ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ =====

if __name__ == "__main__":
    # Пример 1: Simple случай
    pts1 = [
        (0, 3),
        (1, 1),
        (2, 2),
        (4, 4),
        (0, 0),
        (1, 2),
        (3, 1),
        (3, 3),
    ]

    hull1 = graham_scan(pts1)
    print("Пример 1: Выпуклая оболочка")
    print(f"Входные точки: {pts1}")
    print(f"Выпуклая оболочка: {hull1}")

    # Пример 2: Квадрат с центром
    pts2 = [
        (0, 0),
        (10, 0),
        (10, 10),
        (0, 10),
        (5, 5),  # центр, не в оболочке
    ]

    hull2 = graham_scan(pts2)
    print(f"\nПример 2: Квадрат с центром")
    print(f"Входные точки: {pts2}")
    print(f"Выпуклая оболочка: {hull2}")

    # Пример 3: Коллинеарные точки (в линию)
    pts3 = [(0, 0), (1, 1), (2, 2), (3, 3)]

    hull3 = graham_scan(pts3)
    print(f"\nПример 3: Коллинеарные точки")
    print(f"Входные точки: {pts3}")
    print(f"Выпуклая оболочка: {hull3}")
