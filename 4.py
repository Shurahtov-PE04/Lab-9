import os
import heapq
from typing import List


class ExternalMergeSort:
    """
    Класс для сортировки больших файлов, которые не помещаются в ОЗУ.

    Атрибуты:
        chunk_size: максимальное количество строк в одном куске,
                   загружаемом в память
    """

    def __init__(self, chunk_size: int = 100_000):
        """
        Инициализация сортировщика.

        Args:
            chunk_size: размер одного блока (в строках)
        """
        self.chunk_size = chunk_size

    def _create_sorted_chunks(self, input_file: str) -> List[str]:
        """
        Фаза 1: Чтение входного файла, разбиение на куски
        и сортировка каждого куска.

        Args:
            input_file: путь к входному файлу

        Returns:
            Список имён временных файлов с отсортированными кусками
        """
        temp_files = []
        chunk = []
        file_counter = 0

        # S1-S9: Читаем файл и разбиваем на куски
        with open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                chunk.append(line.rstrip("\n"))

                # S5: Если кусок заполнен, сортируем и сохраняем его
                if len(chunk) >= self.chunk_size:
                    chunk.sort()  # S6

                    # S7: Записываем в временный файл
                    temp_name = f"temp_{file_counter}.txt"
                    with open(temp_name, "w", encoding="utf-8") as tf:
                        for item in chunk:
                            tf.write(item + "\n")
                    temp_files.append(temp_name)
                    chunk = []
                    file_counter += 1

        # S8-S9: Обработка последнего неполного куска (если он есть)
        if chunk:
            chunk.sort()
            temp_name = f"temp_{file_counter}.txt"
            with open(temp_name, "w", encoding="utf-8") as tf:
                for item in chunk:
                    tf.write(item + "\n")
            temp_files.append(temp_name)

        return temp_files

    def _merge_chunks(self, temp_files: List[str], output_file: str) -> None:
        """
        Фаза 2: Многопутевое слияние отсортированных кусков в один файл.

        Args:
            temp_files: список имён временных файлов
            output_file: путь к выходному файлу
        """
        # S11: Открываем все временные файлы
        files = [open(name, "r", encoding="utf-8") for name in temp_files]

        # S12: Инициализируем min-heap (куча)
        # Каждый элемент: (значение, индекс файла)
        heap = []

        # S12: Добавляем первую строку из каждого файла
        for i, f in enumerate(files):
            line = f.readline()
            if line:
                heapq.heappush(heap, (line.rstrip("\n"), i))

        # S13-S15: Основной цикл многопутевого слияния
        with open(output_file, "w", encoding="utf-8") as out:
            while heap:
                # S14: Извлекаем минимальную строку
                value, idx = heapq.heappop(heap)
                out.write(value + "\n")

                # S15: Читаем следующую строку из того же файла
                next_line = files[idx].readline()
                if next_line:
                    heapq.heappush(heap, (next_line.rstrip("\n"), idx))

        # S16: Закрываем файлы и удаляем временные файлы
        for f in files:
            f.close()
        for name in temp_files:
            os.remove(name)

    def sort_file(self, input_file: str, output_file: str) -> None:
        """
        Полный процесс сортировки большого файла.

        Args:
            input_file: путь к входному файлу
            output_file: путь к выходному файлу
        """
        print(f"Начало сортировки файла: {input_file}")

        # Фаза 1: Разбиение и сортировка кусков
        print("Фаза 1: Разбиение на куски и их сортировка...")
        temp_files = self._create_sorted_chunks(input_file)
        print(f"Создано {len(temp_files)} отсортированных кусков")

        # Фаза 2: Слияние кусков
        print("Фаза 2: Слияние отсортированных кусков...")
        self._merge_chunks(temp_files, output_file)

        print(f"Сортировка завершена. Результат в {output_file}")


# ===== ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ =====

if __name__ == "__main__":
    # Создание тестового файла с неупорядоченными данными
    test_data = [
        "banana",
        "apple",
        "cherry",
        "date",
        "elderberry",
        "fig",
        "grape",
        "honeydew",
        "iris",
        "jackfruit",
        "kiwi",
        "lemon",
    ]

    input_filename = "test_input.txt"
    output_filename = "test_sorted.txt"

    # Создаём входной файл
    with open(input_filename, "w") as f:
        for item in test_data:
            f.write(item + "\n")

    print(f"Создан тестовый файл: {input_filename}")
    print(f"Исходные данные: {test_data}\n")

    # Выполняем внешнюю сортировку (chunk_size=4 для наглядности)
    sorter = ExternalMergeSort(chunk_size=4)
    sorter.sort_file(input_filename, output_filename)

    # Читаем отсортированный результат
    print(f"\nОтсортированные данные из {output_filename}:")
    with open(output_filename, "r") as f:
        sorted_data = [line.rstrip("\n") for line in f]
        for item in sorted_data:
            print(f"  {item}")

    # Очистка (удаляем тестовые файлы)
    if os.path.exists(input_filename):
        os.remove(input_filename)
    if os.path.exists(output_filename):
        os.remove(output_filename)

    print("\nТестовые файлы удалены.")