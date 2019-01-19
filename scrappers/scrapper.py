import logging
import requests
import json
import datetime as dt
import time

logger = logging.getLogger(__name__)


class Scrapper(object):
    def __init__(self, skip_objects=None):
        self.skip_objects = skip_objects

    def scrap_process(self, storage):

        # You can iterate over ids, or get list of objects
        # from any API, or iterate throught pages of any site
        # Do not forget to skip already gathered data
        # Here is an example for you
        url = 'https://api.opendota.com/api/'

        team_ids = self.scrap_teams(url)
        print(str(len(team_ids)) + ' teams to process. Please wait')
        time.sleep(1)

        match_ids = []
        for i in range(len(team_ids)):
            team_matches = self.scrap_team_matches(url, team_ids[i])
            match_ids += team_matches
            print('team ' + str(i + 1) + ' out of ' + str(len(team_ids)) + ' processed')
            time.sleep(1)

        match_ids = list(set(match_ids))
        print(str(len(match_ids)) + ' matches to process. Please wait')

        matches = []
        for i in range(len(match_ids)):
            matches.append(self.scrap_match(url, match_ids[i]))
            print('match ' + str(i + 1) + ' out of ' + str(len(match_ids)) + ' processed')
            time.sleep(1)

        with open(storage, 'w') as store:
            store.write(json.dumps(matches, sort_keys=True, indent=4))

    #выбираем профессиональные команды, которые играли в период последних трех месяцев и имеют счетчик игр больше 100
    def scrap_teams(self, url):
        response = requests.get(url + 'teams')

        if not response.ok:
            logger.error(response.text)

        else:
            data = response.json()
            three_months_ago = (dt.datetime.now() - dt.timedelta(days=90)).timestamp()
            active_pro_team_ids = []
            for team in data:
                if team['wins'] + team['losses'] > 100 and team['last_match_time'] > three_months_ago:
                    active_pro_team_ids.append(team['team_id'])

            return active_pro_team_ids

    #находим id матчей, сыгранных командой
    #выбираем матчи за последние 3 месяца
    def scrap_team_matches(self, url, id):
        response = requests.get(url + 'teams/' + str(id) + '/matches')

        if not response.ok:
            logger.error(response.text)

        else:
            data = response.json()
            three_months_ago = (dt.datetime.now() - dt.timedelta(days=90)).timestamp()
            match_ids_played = []
            for match in data:
                if match['start_time'] > three_months_ago:
                    match_ids_played.append(match['match_id'])

            return match_ids_played

    def scrap_match(self, url, id):
        response = requests.get(url + 'matches/' + str(id))

        if not response.ok:
            logger.error(response.text)

        else:
            data = response.json()

            useful_data = {}
            for key, value in data.items():
                if key == 'match_id' or key == 'dire_score' or key == 'radiant_score' or \
                                key == 'radiant_win' or key == 'radiant_team' or key == 'dire_team' or \
                                key == 'start_time' or key == 'players':
                    useful_data[key] = value
            return useful_data

if __name__ == '__main__':
    scrapper = Scrapper()
    scrapper.scrap_process('test.json')