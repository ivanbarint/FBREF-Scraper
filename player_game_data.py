def home_game_stats(comp, year, home_team, away_team):
    
    import scores_and_fixtures
    import check_name
    from get_position import get_basic_position, get_detailed_position
    from datetime import datetime
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    from collections import defaultdict

    results_df = scores_and_fixtures.season_results_and_fixtures(comp, year)
    home_team = check_name.get_team_name(home_team)
    away_team = check_name.get_team_name(away_team)
    
    for i, row in results_df.iterrows():
        if row['home_team'] == home_team and row['away_team'] == away_team:
            url = f"https://fbref.com/{row['match_url']}"
            resp = requests.get(url) 
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text.replace('<!--', '').replace('--!>', ''), 'html.parser')
            
            tables = soup.find_all('table', {'class':'stats_table sortable'})
            tbodies = soup.find_all('tbody')
            
            home_team_id = tables[0].get('id').split('_')[1]
            away_team_id = tables[-1].get('id').split('_')[1]
            
            for table in tables:
                if table.get('id').split('_')[1] == home_team_id:
                    player_ids, player_names = [], []
                    
                    th = table.find_all('th', {'data-stat':'player'})
                    
                    for h in th:
                        if player_ids.append(h.get('data-append-csv')) not in player_ids:
                            player_ids.append(h.get('data-append-csv'))
                        if player_names.append(h.get('csk')) not in player_names:
                            player_names.append(h.get('csk'))
                            
                    df = pd.DataFrame(list(zip(player_ids, player_names)), columns = ['player_id', 'player'])
                    df = df.drop(df.index[0]).reset_index(drop = True)
                    df = df[:-1].reset_index(drop = True)
            
            for table in tables:
                if table.get('id').split('_')[1] == home_team_id:
                    headers, full_player_values = [], []
                    rows = table.find_all('tr')
                    
                    row_for_headers = rows[-1].find_all('td')
                    
                    for value in row_for_headers:
                        headers.append(value.get('data-stat'))
                    
                    for row in rows:
                        player_values = []
                        data = row.find_all('td')
                        for value in data:
                            player_values.append(value.get_text())
                        full_player_values.append(player_values)
                        
                    data_df = pd.DataFrame(full_player_values, columns = headers)
                    data_df = data_df.dropna()
                    data_df = data_df[:-1].reset_index(drop = True)
                    
                    df = pd.concat([df, data_df], axis = 1)
                    
            df = df.loc[:, ~df.columns.duplicated()]
            
            df = df.apply(pd.to_numeric, errors = 'ignore') 
            
            df = df.fillna(0)
            
            return df
        
        
def away_game_stats(comp, year, home_team, away_team):
    
    import scores_and_fixtures
    import check_name
    from get_position import get_basic_position, get_detailed_position
    from datetime import datetime
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    from collections import defaultdict

    results_df = scores_and_fixtures.season_results_and_fixtures(comp, year)
    home_team = check_name.get_team_name(home_team)
    away_team = check_name.get_team_name(away_team)
    
    for i, row in results_df.iterrows():
        if row['home_team'] == home_team and row['away_team'] == away_team:
            url = f"https://fbref.com/{row['match_url']}"
            resp = requests.get(url) 
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text.replace('<!--', '').replace('--!>', ''), 'html.parser')
            
            tables = soup.find_all('table', {'class':'stats_table sortable'})
            tbodies = soup.find_all('tbody')
            
            home_team_id = tables[0].get('id').split('_')[1]
            away_team_id = tables[-1].get('id').split('_')[1]
            
            for table in tables:
                if table.get('id').split('_')[1] == away_team_id:
                    player_ids, player_names = [], []
                    
                    th = table.find_all('th', {'data-stat':'player'})
                    
                    for h in th:
                        if player_ids.append(h.get('data-append-csv')) not in player_ids:
                            player_ids.append(h.get('data-append-csv'))
                        if player_names.append(h.get('csk')) not in player_names:
                            player_names.append(h.get('csk'))
                            
                    df = pd.DataFrame(list(zip(player_ids, player_names)), columns = ['player_id', 'player'])
                    df = df.drop(df.index[0]).reset_index(drop = True)
                    df = df[:-1].reset_index(drop = True)
            
            for table in tables:
                if table.get('id').split('_')[1] == away_team_id:
                    headers, full_player_values = [], []
                    rows = table.find_all('tr')
                    
                    row_for_headers = rows[-1].find_all('td')
                    
                    for value in row_for_headers:
                        headers.append(value.get('data-stat'))
                    
                    for row in rows:
                        player_values = []
                        data = row.find_all('td')
                        for value in data:
                            player_values.append(value.get_text())
                        full_player_values.append(player_values)
                        
                    data_df = pd.DataFrame(full_player_values, columns = headers)
                    data_df = data_df.dropna()
                    data_df = data_df[:-1].reset_index(drop = True)
                    
                    df = pd.concat([df, data_df], axis = 1)
                    
            df = df.loc[:, ~df.columns.duplicated()]
            
            df = df.apply(pd.to_numeric, errors = 'ignore') 
            
            df = df.fillna(0)
            
            return df