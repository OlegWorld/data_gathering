# data_gathering
otus data science hw1

В задании производится анализ статистики матчей профессиональных команд по dota2.

На этапе скрэппинга производится сбор данных о командах с api сайта opendota.com:
Запрашиваются данные о командах, из полученного списка выбираются профессиональные команды. Профессиональными считаются те команды, которые играли в течении последних трех месяцев и у которых количество зарегистрированных на сайте матчей более 100.
Для отобранных команд выбираются данные о матчах сыгранных за последние три месяца.
Из этих данных запоминаются в json файл следующие: счет обеих сыгравших команд, названия команд, победитель, дата и время начала матча, данные об игроках.

На этапе конвертации производится конвертация данных из .json в .csv. При этом производится дополнительная фильтрация сырых данных, а именно: Из данных об игроках выбираются данных о выбранном игроком игровом персонаже (его id)

На этапе построения статистики производится построение статистических данных о частоте выбора каждого игрового персонажа в рамках анализируемых матчей, строится соответствующий график для отсортированных данных
