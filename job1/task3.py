import numpy as np
from functools import reduce


def is_increase(s: list) -> bool:
    """
    Проверяем возрастают ли числа в массиве.
    :param s: Массив
    :return: True - все хорошо массив нормальный. False - есть наложение на отрезках, нужно чинить.
    """
    return all(c < n for c, n in zip(s, s[1:]))


def check_fix_prep_data(arr):
    """
    Проверяет, чинит и приготавливает массив к работе.
    :param arr: Массив
    :return: Полностью готовый к работе массив.
    """

    # Создаем пары (start, end) и сортируем их по первому значению.
    s = [[k, v] for k, v in zip(arr[0::2], arr[1::2])]
    s = sorted(s, key=lambda x: x[0])

    # Проверяем на надобность починки.
    if is_increase(arr):
        return s

    # Валидный массив
    s_true = [s[0]]

    # Начинаем ремонт
    for i in range(0, len(s) - 1):

        for j in range(i, len(s) - 1):
            # Если следующий интервал полностью находится в предедущем, мы его пропускаем
            if s[j][0] in range(s_true[i][0], s_true[i][1] + 1) and s[j][1] in range(s_true[i][0], s_true[i][1] + 1):
                continue
            # Если start из следующего интервала находится в предедущем, а его end больше. чем у предедущего,
            # то обновляем end, у первого.
            elif s[j][0] in range(s_true[i][0], s_true[i][1] + 1) and s[j][1] > s_true[i][i]:
                s_true[i][1] = s[j][1]

            # Если следующий start > предедущего end, то добавляем новый интервал в s_true
            elif s[j][0] > s_true[i][1]:
                s_true.append(s[j])
                break

        # Избегаем out of range
        if i + 1 >= len(s_true):
            break

    return s_true


def calc_delta(x: np.array) -> int:
    """
    Считаем сколько прошло секунд на данном интервале.
    :param x: Интервал
    :return: Сколько прошло секунд
    """
    return x[-1] - x[0]


def appearance(intervals: dict[str:list[int]]) -> int:
    """
    Обрабатывает запрос и считает общее совместное время присудствия ученика и учителя на уроке.
    :param intervals: Интервалы
    :return: Совместное время в секундах
    """
    result = []
    buff = check_fix_prep_data(intervals['lesson'])
    pupils = check_fix_prep_data(intervals['pupil'])
    tutors = check_fix_prep_data(intervals['tutor'])

    # Создаем интервал урока
    lesson_interval = np.arange(buff[0][0], buff[0][1] + 1)

    # Парные переборы по отрезкам
    for tutor_start, tutor_end in tutors:
        # Создаем интервал учителя
        tutor_interval = np.arange(tutor_start, tutor_end + 1)
        for pupil_start, pupil_end in pupils:
            # Создаем интервал ученика
            pupil_interval = np.arange(pupil_start, pupil_end + 1)
            # Ищем пересечения и добавляем их в результаты
            result.append(reduce(np.intersect1d, (pupil_interval, tutor_interval, lesson_interval)))

    # Используем list compression, и считаем интересующий нас результат
    result = [calc_delta(arr) for arr in result if arr.size > 0]
    return sum(result)


tests = [
    {'data': {'lesson': [1594663200, 1594666800],
              'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
              'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'data': {'lesson': [1594702800, 1594706400],
              'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150,
                        1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480,
                        1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
                        1594706524, 1594706524, 1594706579, 1594706641],
              'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'data': {'lesson': [1594692000, 1594695600],
              'pupil': [1594692033, 1594696347],
              'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['data'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'