# data_gathering
otus data science hw1

В задании производится анализ статистики матчей профессиональных команд по dota2.

На этапе скрэппинга производится сбор данных о командах с api сайта opendota.com:
Запрашиваются данные о командах, из полученного списка выбираются профессиональные команды. Профессиональными считаются те команды, которые играли в течении последних трех месяцев и у которых количество зарегистрированных на сайте матчей более 100.
Для отобранных команд выбираются данные о матчах сыгранных за последние три месяца.
Из этих данных запоминаются в json файл следующие: счет обеих сыгравших команд, названия команд, победитель, дата и время начала матча, данные об игроках.

На этапе конвертации производится конвертация данных из .json в .csv. При этом производится дополнительная фильтрация сырых данных, а именно: Из данных об игроках выбираются данных о выбранном игроком игровом персонаже (его id)

На этапе построения статистики производятся:
- подсчет суммарного количества матчей и количество выигрышей каждой фракции (dire - radiant) (wins_count)
- определение команды с наибольшим числом побед (most_winning_team)
- построение статистики очков фракций за матч (с вычислением мат. ожидания и СКО) (score_count)
- построение статистических данных о частоте выбора каждого игрового персонажа командами-победителями в рамках анализируемых матчей, строится соответствующий график для отсортированных данных (hero_stats)

P.S. В матче dota2 сражаются две фракции - radiant и dire, как в шахматах белые и черные фигуры. Две играющие команды в начале игры приписываются к одной из фракций. Часть статистик, соответственно, приведена для этих самых фракций - dire и radiant
