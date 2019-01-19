"""
ЗАДАНИЕ

Выбрать источник данных и собрать данные по некоторой предметной области.

Цель задания - отработать навык написания программ на Python.
В процессе выполнения задания затронем области:
- организация кода в виде проекта, импортирование модулей внутри проекта
- unit тестирование
- работа с файлами
- работа с протоколом http
- работа с pandas
- логирование

Требования к выполнению задания:

- собрать не менее 1000 объектов

- в каждом объекте должно быть не менее 5 атрибутов
(иначе просто будет не с чем работать.
исключение - вы абсолютно уверены что 4 атрибута в ваших данных
невероятно интересны)

- сохранить объекты в виде csv файла

- считать статистику по собранным объектам


Этапы:

1. Выбрать источник данных.

Это может быть любой сайт или любое API

Примеры:
- Пользователи vk.com (API)
- Посты любой популярной группы vk.com (API)
- Фильмы с Кинопоиска
(см. ссылку на статью ниже)
- Отзывы с Кинопоиска
- Статьи Википедии
(довольно сложная задача,
можно скачать дамп википедии и распарсить его,
можно найти упрощенные дампы)
- Статьи на habrahabr.ru
- Объекты на внутриигровом рынке на каком-нибудь сервере WOW (API)
(желательно англоязычном, иначе будет сложно разобраться)
- Матчи в DOTA (API)
- Сайт с кулинарными рецептами
- Ebay (API)
- Amazon (API)
...

Не ограничивайте свою фантазию. Это могут быть любые данные,
связанные с вашим хобби, работой, данные любой тематики.
Задание специально ставится в открытой форме.
У такого подхода две цели -
развить способность смотреть на задачу широко,
пополнить ваше портфолио (вы вполне можете в какой-то момент
развить этот проект в стартап, почему бы и нет,
а так же написать статью на хабр(!) или в личный блог.
Чем больше у вас таких активностей, тем ценнее ваша кандидатура на рынке)

2. Собрать данные из источника и сохранить себе в любом виде,
который потом сможете преобразовать

Можно сохранять страницы сайта в виде отдельных файлов.
Можно сразу доставать нужную информацию.
Главное - постараться не обращаться по http за одними и теми же данными много раз.
Суть в том, чтобы скачать данные себе, чтобы потом их можно было как угодно обработать.
В случае, если обработать захочется иначе - данные не надо собирать заново.
Нужно соблюдать "этикет", не пытаться заддосить сайт собирая данные в несколько потоков,
иногда может понадобиться дополнительная авторизация.

В случае с ограничениями api можно использовать,
чтобы сделать задержку между запросами

3. Преобразовать данные из собранного вида в табличный вид.

Нужно достать из сырых данных ту самую информацию, которую считаете ценной
и сохранить в табличном формате - csv отлично для этого подходит

4. Посчитать статистики в данных
Требование - использовать pandas (мы ведь еще отрабатываем навык использования инструментария)
То, что считаете важным и хотели бы о данных узнать.

Критерий сдачи задания - собраны данные по не менее чем 1000 объектам (больше - лучше),
при запуске кода командой "python3 -m gathering stats" из собранных данных
считается и печатается в консоль некоторая статистика

Код можно менять любым удобным образом
Можно использовать и Python 2.7, и 3

Зачем нужны __init__.py файлы
https://stackoverflow.com/questions/448271/what-is-init-py-for

Про документирование в Python проекте
https://www.python.org/dev/peps/pep-0257/

Про оформление Python кода
https://www.python.org/dev/peps/pep-0008/


Примеры сбора данных:
https://habrahabr.ru/post/280238/

Для запуска тестов в корне проекта:
python3 -m unittest discover

Для запуска проекта из корня проекта:
python3 -m gathering gather
или
python3 -m gathering transform
или
python3 -m gathering stats


Для проверки стиля кода всех файлов проекта из корня проекта
pep8 .

"""

import logging

import sys
import json
import pandas as pd
import requests
import matplotlib.pyplot as plt

from scrappers.scrapper import Scrapper
from storages.file_storage import FileStorage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SCRAPPED_FILE = 'scrapped_data.json'
TABLE_FORMAT_FILE = 'data.csv'


def gather_process():
    logger.info("gather")
    scrapper = Scrapper()
    scrapper.scrap_process(SCRAPPED_FILE)

def convert_data_to_table_format():
    logger.info("transform")

    import csv

    data = None
    with open(SCRAPPED_FILE, 'r') as in_file:
        data = json.loads(in_file.read())

    with open(TABLE_FORMAT_FILE, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file,
                                delimiter='\t',
                                quotechar='"',
                                escapechar=' ',
                                quoting=csv.QUOTE_NONE)
        csv_writer.writerow(['match_id',
                             'radiant_team',
                             'dire_team',
                             'radiant_score',
                             'dire_score',
                             'radiant_win',
                             'radiant_pick',
                             'dire_pick'
                             ])
        for match in data:
            if match:
                row = [match['match_id'], match['radiant_team']['name'], match['dire_team']['name'],
                       match['radiant_score'], match['dire_score'], match['radiant_win']]

                radiant_pick = []
                dire_pick = []
                for i in range(10):
                    if match['players'][i]['isRadiant']:
                        radiant_pick.append(match['players'][i]['hero_id'])
                    else:
                        dire_pick.append(match['players'][i]['hero_id'])

                row.append(radiant_pick)
                row.append(dire_pick)

                csv_writer.writerow(row)

def stats_data():
    logger.info("stats")

    matches_stat = pd.read_csv('data.csv', sep='\t')
    int_list = [[int(i) for i in j[1:-1].split(',  ')] for j in matches_stat['radiant_pick']]
    matches_stat['radiant_pick'] = int_list
    int_list = [[int(i) for i in j[1:-1].split(',  ')] for j in matches_stat['dire_pick']]
    matches_stat['dire_pick'] = int_list
    del int_list

    # let's see, for example, the pick distribution for winners
    radiant_win_stat = matches_stat[matches_stat['radiant_win']]
    dire_win_stat = matches_stat[matches_stat['radiant_win'] == False]

    radiant_win_pick = radiant_win_stat['radiant_pick']
    dire_win_pick = dire_win_stat['dire_pick']
    winning_heroes = radiant_win_pick.sum() + dire_win_pick.sum()

    winning_hero_distr = {}
    for hero in winning_heroes:
        if hero in winning_hero_distr:
            winning_hero_distr[hero] += 1 / len(winning_heroes)
        else:
            winning_hero_distr[hero] = 1 / len(winning_heroes)

    #let's get hero names for better view
    result = requests.get('https://api.opendota.com/api/heroes')
    data = result.json()
    names = []
    for hero in data:
        names.append(hero['localized_name'])

    hero_stat = pd.DataFrame.from_dict(winning_hero_distr, orient='index')
    hero_stat.columns = ['hero_picks']
    hero_stat.index = names

    hero_stat.sort_values('hero_picks', ascending=False).plot(kind='bar')
    plt.show()

if __name__ == '__main__':
    logger.info("Work started")

    if sys.argv[1] == 'gather':
        gather_process()

    elif sys.argv[1] == 'transform':
        convert_data_to_table_format()

    elif sys.argv[1] == 'stats':
        stats_data()

    logger.info("work ended")
