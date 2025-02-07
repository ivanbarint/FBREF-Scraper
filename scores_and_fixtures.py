def season_results_and_fixtures(competition, year):
    import pandas as pd
    import check_comp
    import requests
    from bs4 import BeautifulSoup
    from datetime import datetime

    comp = check_comp.check_comp(competition) 
    season = f"{str(year)}-{str(year+1)}"
    url = f"https://fbref.com/en/comps/{comp[0]}/{season}/schedule/{season}-{comp[1]}-Scores-and-Fixtures"

    resp = requests.get(url) 
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text.replace('<!--', '').replace('--!>', ''), 'html.parser')

    headers, rows, match_urls = [], [], []

    table_data = soup.find_all('tbody')[0]
    table_rows = table_data.find_all('tr')

    for value in table_rows[0]:
        headers.append(value.get('data-stat'))

    for row in table_rows:
        row_values = []
        row_header = row.find('th').get_text()
        row_values.append(row_header)
        row_data = row.find_all('td')
        for data_value in row_data: 
            row_values.append(data_value.get_text())
        
        try:
            match_urls.append(row.find('td', {'data-stat':'score'}).a.get('href'))
        except: pass
        
        rows.append(row_values)

    df = pd.DataFrame(rows, columns = headers)
    
    ## df['attendance'] = df['attendance'].str.replace(',', '').replace('', 0).astype(int)
    df = df.apply(pd.to_numeric, errors='ignore')

    df = df[df['date'] != ""].reset_index(drop=True)

    df['date'] = pd.to_datetime(df['date'])

    df[['home_score', 'away_score']] = df['score'].str.split('–', expand=True)
    df['home_score'] = pd.to_numeric(df['home_score'], errors='coerce')
    df['away_score'] = pd.to_numeric(df['away_score'], errors='coerce')

    df['date'] = pd.to_datetime(df['date'].astype(str))
    
    proper_order = ['gameweek', 'dayofweek', 'date', 'start_time', 'home_team', 'home_xg', 'home_score', 'away_score', 'away_xg', 'away_team', 'attendance', 'venue', 'referee', 'match_report', 'notes']
    
    df = df[proper_order]
    
    df['match_url'] = pd.Series(match_urls)
    
    return df