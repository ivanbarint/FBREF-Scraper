def player_stats(competition, year, data_type):
    
    import pandas as pd
    import check_comp
    import requests
    from bs4 import BeautifulSoup
    
    try:
        comp = check_comp.check_comp(competition) 
        season = f"{str(year)}-{str(year+1)}"
        url = f"https://fbref.com/en/comps/{comp[0]}/{season}/{data_type}/{season}-{comp[1]}-Stats"

        resp = requests.get(url) 
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text.replace('<!--', '').replace('--!>', ''), 'html.parser')
        
        headers, rows = [], []

        table_data = soup.find_all('tbody')[2]
        table_rows = table_data.find_all('tr')

        for value in table_rows[0]:
            headers.append(value.get('data-stat'))

        for row in table_rows:
            row_values = []
            row_data = row.find_all('td')
            for data_value in row_data:
                if data_value.get('data-append-csv'):
                    row_values.append(data_value.get('data-append-csv')) 
                row_values.append(data_value.get_text())
            rows.append(row_values)

        df = pd.DataFrame(rows, columns = headers).fillna(0) 
        df = df.loc[df['player'] != 0].reset_index(drop = True) 
        
        if 'minutes' in headers:
            df['minutes'] = df['minutes'].str.replace(',', '')
        elif 'gk_minutes' in headers:
            df['gk_minutes'] = df['gk_minutes'].str.replace(',', '')
      
        for i, row in df.iterrows():
            try:
                if '-' in row['age']:
                    age_num = row['age'].split('-')[0] 
                    df.at[i, 'age'] = age_num 
            except Exception: pass 

        df.rename(columns={'ranker' : 'player_id'}, inplace=True) 
        df = df.apply(pd.to_numeric, errors = 'ignore') 
        return df 
    
    except: return "Invalid data input"

def full_keeper_stats(competition, year):
    
    import pandas as pd
    from internal_packages import check_comp
    import requests
    from bs4 import BeautifulSoup
    
    keeper_data_types = ['keepers', 'keepersadv']
    
    df = pd.DataFrame()
        
    try:
        comp = check_comp.check_comp(competition) 
        season = f"{str(year)}-{str(year+1)}"
        
        for d_type in keeper_data_types:
            url = f"https://fbref.com/en/comps/{comp[0]}/{season}/{d_type}/{season}-{comp[1]}-Stats" 
            resp = requests.get(url) 
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text.replace('<!--', '').replace('--!>', ''), 'html.parser')

            headers, rows = [], []

            table_data = soup.find_all('tbody')[2]
            table_rows = table_data.find_all('tr')

            for value in table_rows[0]:
                headers.append(value.get('data-stat'))

            for row in table_rows:
                row_values = []
                row_data = row.find_all('td')
                for data_value in row_data:
                    if data_value.get('data-append-csv'):
                        row_values.append(data_value.get('data-append-csv')) 
                    row_values.append(data_value.get_text())
                rows.append(row_values)

            data_df = pd.DataFrame(rows, columns = headers).fillna(0) 
            data_df = data_df.loc[data_df['player'] != 0].reset_index(drop = True) 
            if 'minutes' in headers:
                data_df['minutes'] = data_df['minutes'].str.replace(',', '')
            elif 'gk_minutes' in headers:
                data_df['gk_minutes'] = data_df['gk_minutes'].str.replace(',', '')

            for i, row in data_df.iterrows():
                try:
                    if '-' in row['age']:
                        age_num = row['age'].split('-')[0] 
                        data_df.at[i, 'age'] = age_num
                except Exception: pass 
            
            data_df.rename(columns={'ranker' : 'player_id'}, inplace=True) 
            data_df = data_df.apply(pd.to_numeric, errors = 'ignore') 
            
            data_df = data_df.set_index('player_id')
            
            df = pd.concat([df, data_df], axis = 1)
        
        df = df.loc[:,~df.columns.duplicated()]
        
        df = df.reset_index()
        
        return df
            
    except: return "Invalid data input" 
    
def full_player_stats(competition, year):
    
    import pandas as pd
    from internal_packages import check_comp
    import requests
    from bs4 import BeautifulSoup
    
    player_data_types = ['stats', 'shooting', 'passing', 'passing_types', 'gca', 'defense', 'possession', 'playingtime', 'misc']
    
    df = pd.DataFrame()
        
    try:
        comp = check_comp.check_comp(competition) 
        season = f"{str(year)}-{str(year+1)}"
        
        for d_type in player_data_types:
            
            url = f"https://fbref.com/en/comps/{comp[0]}/{season}/{d_type}/{season}-{comp[1]}-Stats" 
            resp = requests.get(url) 
            
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text.replace('<!--', '').replace('--!>', ''), 'html.parser')

            headers, rows = [], []

            table_data = soup.find_all('tbody')[2]
            table_rows = table_data.find_all('tr')

            for value in table_rows[0]:
                headers.append(value.get('data-stat'))

            for row in table_rows:
                row_values = []
                row_data = row.find_all('td')
                for data_value in row_data:
                    if data_value.get('data-append-csv'):
                        row_values.append(data_value.get('data-append-csv')) 
                    row_values.append(data_value.get_text())
                rows.append(row_values)

            data_df = pd.DataFrame(rows, columns = headers) 
    
            data_df = data_df.fillna(0)
            data_df = data_df.loc[data_df['player'] != 0].reset_index(drop = True) 
            
            if 'minutes' in headers:
                data_df['minutes'] = data_df['minutes'].str.replace(',', '')
            elif 'gk_minutes' in headers:
                data_df['gk_minutes'] = data_df['gk_minutes'].str.replace(',', '')

            for i, row in data_df.iterrows():
                try:
                    if '-' in row['age']: 
                        age_num = row['age'].split('-')[0] 
                        data_df.at[i, 'age'] = age_num 
                except Exception: pass 
            
            data_df.rename(columns={'ranker' : 'player_id'}, inplace=True) 
            
            data_df = data_df.apply(pd.to_numeric, errors = 'ignore') 
            
            data_df = data_df.set_index(['player_id', 'team'])
            
            df = pd.concat([df, data_df], axis = 1)
        
        df = df.loc[:, ~df.columns.duplicated()]
        
        df = df.dropna(subset = ['player'])
        
        df = df.reset_index()
        
        return df
            
    except: return "Invalid data input" 