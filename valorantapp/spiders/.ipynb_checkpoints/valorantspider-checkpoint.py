import scrapy
import itertools
import pyodbc

class valorantSpider(scrapy.Spider):
    name = 'VCT'
    start_urls = ['https://www.vlr.gg/stats/?event_group_id=45&event_id=1657&series_id=all&region=all&country=all&min_rounds=0&min_rating=0&agent=all&map_id=all&timespan=all']

    def parse(self, response):
        team_list = response.css('div.stats-player-country::text').getall()
        gamertag_list = response.css('div.text-of::text').getall()
        rounds_list = response.css('td.mod-rnd::text').getall()
        kill_list = response.css('td:nth-child(17)::text').getall()
        death_list = response.css('td:nth-child(18)::text').getall() 
        assist_list = response.css('td:nth-child(19)::text').getall()
        fk_list = response.css('td:nth-child(20)::text').getall()
        fd_list = response.css('td:nth-child(21)::text').getall()
        KAST_list = response.css('td:nth-child(7) span::text').getall()
        ACS_list = response.css('td.mod-color-sq.mod-acs span::text').getall()
        hs_list = response.css('td:nth-child(13) span::text').getall()
        kmax_list = response.css('td.mod-a.mod-kmax a::text').getall()
        kmax_clean_list = [text.strip() for text in kmax_list]

        master_list = [team_list, gamertag_list, rounds_list, kill_list, death_list, assist_list, fk_list, fd_list, KAST_list, ACS_list, hs_list, kmax_clean_list]

        for data in itertools.zip_longest(*master_list):
            team, gamertag, rounds, kills, deaths, assists, fks, fds, kast, acs, hs, kmax = data
            yield {
            'team': team,
            'gamertag': gamertag,
            'rounds': rounds,
            'kills': kills,
            'deaths': deaths,
            'assists': assists,
            'fks': fks,
            'fds': fds,
            'kast': kast,
            'acs': acs,
            'hs': hs,
            'kmax': kmax
        }
            
        connection_string = (
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=valorant-hp.database.windows.net;'
            r'DATABASE=VALORANT_HP;'
            r'UID=hieuphan;'
            r'PWD=Aliyaceniceros1!'
        )
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        for data in itertools.zip_longest(*master_list):
            team, gamertag, rounds, kills, deaths, assists, fks, fds, kast, acs, hs, kmax = data

            insert_query = """
            INSERT INTO vctstats (team, gamertag, rounds, kills, deaths, assists, fks, fds, kast, acs, hs, kmax)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            values = (team, gamertag, rounds, kills, deaths, assists, fks, fds, kast, acs, hs, kmax)
            cursor.execute(insert_query, values)
            conn.commit()

        conn.close()