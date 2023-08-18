import scrapy
import itertools
import mysql.connector

class ValorantSpider(scrapy.Spider):
    name = 'VCT'
    start_urls = ['https://www.vlr.gg/stats/?event_group_id=45&event_id=1657&series_id=all&region=all&country=all&min_rounds=0&min_rating=1550&agent=all&map_id=all&timespan=30d']

    def parse(self, response):
        team_list = response.css('div.stats-player-country::text').getall()
        gamertag_list = response.css('div.text-of::text').getall()

        lysoar_index = gamertag_list.index("Lysoar")
        team_list.insert(lysoar_index, None)

        rounds_list = response.css('td.mod-rnd::text').getall()
        kill_list = response.css('td:nth-child(17)::text').getall()
        death_list = response.css('td:nth-child(18)::text').getall()
        assist_list = response.css('td:nth-child(19)::text').getall()
        fk_list = response.css('td:nth-child(20)::text').getall()
        fd_list = response.css('td:nth-child(21)::text').getall()
        kast_list = response.css('td:nth-child(7) span::text').getall()
        acs_list = response.css('td.mod-color-sq.mod-acs span::text').getall()
        hs_list = response.css('td:nth-child(13) span::text').getall()
        kmax_list = response.css('td.mod-a.mod-kmax a::text').getall()
        kmax_clean_list = [text.strip() for text in kmax_list]

        master_list = [team_list, gamertag_list, rounds_list, kill_list, death_list, assist_list, fk_list, fd_list, kast_list, acs_list, hs_list, kmax_clean_list]

        connection = mysql.connector.connect(
            host=self.settings.get('DATABASE_HOST'),
            user=self.settings.get('DATABASE_USER'),
            password=self.settings.get('DATABASE_PASSWORD'),
            database=self.settings.get('DATABASE_NAME')
        )

        cursor = connection.cursor()

        truncate_query = "TRUNCATE TABLE vctChampionsOverallPlayerStats"
        cursor.execute(truncate_query)
        connection.commit()

        for data in itertools.zip_longest(*master_list):
            team, gamertag, rounds, kills, deaths, assists, fks, fds, kast, acs, hs, kmax = data
            """
            yield {
                'team': team if team != 'NULL' else None,
                'gamertag': gamertag if gamertag else None,
                'rounds': int(rounds) if rounds else None,
                'kills': int(kills) if kills else None,
                'deaths': int(deaths) if deaths else None,
                'assists': int(assists) if assists else None,
                'fks': int(fks) if fks else None,
                'fds': int(fds) if fds else None,
                'kast': float(kast.rstrip('%')) / 100 if kast else None,
                'acs': float(acs) if acs else None,
                'hs': float(hs.rstrip('%')) / 100 if hs else None,
                'kmax': int(kmax) if kmax else None
            }
            """
            values = (
                team if team != 'NULL' else None,
                gamertag if gamertag else None,
                int(rounds) if rounds else None,
                int(kills) if kills else None,
                int(deaths) if deaths else None,
                int(assists) if assists else None,
                int(fks) if fks else None,
                int(fds) if fds else None,
                float(kast.rstrip('%')) / 100 if kast else None,
                float(acs) if acs else None,
                float(hs.rstrip('%')) / 100 if hs else None,
                int(kmax) if kmax else None
            )

            insert_query = """
            INSERT INTO vctChampionsOverallPlayerStats (team, gamertag, rounds, kills, deaths, assists, fks, fds, kast, acs, hs, kmax)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, values)
            connection.commit()

        connection.close()
