from bs4 import BeautifulSoup
import requests
import os
import pickle
import pymorphy2

# Ссылки для парсинга
URL = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
WIKI_HEAD = 'https://ru.wikipedia.org'

# Морфологический анализатор для нормализации слов.
MORPH = pymorphy2.MorphAnalyzer()


def grab_animal_from_page(soup: BeautifulSoup) -> list[str]:
    """
    Парсим всех животных с данной странице
    :param soup: Страница в супе
    :return: Список с животными
    """
    table = soup.find(id='mw-pages')
    data = table.find_all('li')
    return [i.a['title'] for i in data]  # i - Класс Tag (<li>), а - класс, title - нужное нам значение.


def parse(start_url: str) -> list[str]:
    """
    Парсим Википедию
    :param start_url: Начальная страница со списком животных
    :return: Список со всеми полученными животными
    """
    result = []
    next_url = start_url
    # Обходим все странички.
    while next_url is not None:
        # Парсим страницу
        resp = requests.get(next_url)
        soup = BeautifulSoup(resp.content, 'html.parser')

        # Парсим животных
        result.extend(grab_animal_from_page(soup))

        # Парсим href на некст страницу. Если её нет выходим из цикла
        tag = soup.find('a', string='Следующая страница')
        if tag:
            print('Страница найдена продолжаю парсить.')
            next_url = '{}{}'.format(WIKI_HEAD, tag['href'])
            result.append(next_url)
        else:
            print('Следующая страница не найдена, выхожу из цикла.')
            next_url = None

    return result


def latin_filter_func(x: str) -> bool:
    """
    Проверяем на кирилице ли записано название животного.
    :param x: Животное
    :return: True - на кирилице False - не кирилица
    """
    char = ord(x[0])
    # a-z и A-Z
    if char in range(97, 123) or char in range(65, 91):
        return False
    else:
        return True


def normal_word_map_func(x: str) -> str or None:
    """
    Получаем обычное существительное, если такавово нет, возрщаем None
    :param x: Строка с названием
    :return: str or None Зависит от анализа.
    """
    splited = x.split(' ')
    # Используем обратный массив, чтобы миновать прилагательные в начале, которые не известны анализатору.
    for word in reversed(splited):

        # Если в слове есть скобочки, то мы его пропускаем.
        if word.__contains__('(') or word.__contains__(')'):
            continue

        # Парсим слово
        morp_analyz = MORPH.parse(word)[0]
        # Если слово существительное, то работаем с ним дальше.
        if morp_analyz.tag.POS == 'NOUN':
            return morp_analyz.normal_form.capitalize()

    return None


if __name__ == '__main__':
    # Кешируем, для удобства дебага.
    if os.path.exists('raw_speacies.pickle'):
        # Если пикл файл есть загружаем в память.
        with open('raw_speacies.pickle', 'rb') as f:
            raw_speacies = pickle.load(f)
    else:
        # Если нету парсим,сохраняем,анализируем.
        raw_speacies = parse(URL)
        with open('raw_speacies.pickle', 'wb') as f:
            pickle.dump(raw_speacies, f)

    # Фильтруем сырой список
    speacies = list(filter(latin_filter_func, raw_speacies))

    # Оставляем только нормализованные существительные.
    speacies = list(map(normal_word_map_func, speacies))
    speacies = [i for i in speacies if i is not None]

    # Убираем дубликаты и сортируем.
    speacies = sorted(list(dict.fromkeys(speacies)))

    # Считаем кол-во для каждой буквы
    alphabet_cont_dict = {}
    for speaci in speacies:
        if speaci[0] in alphabet_cont_dict:
            alphabet_cont_dict[speaci[0]] += 1
        else:
            alphabet_cont_dict[speaci[0]] = 1

    # Красиво выводим.
    for key in alphabet_cont_dict:
        print(f'{key}: {alphabet_cont_dict[key]}')