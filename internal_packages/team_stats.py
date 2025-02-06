def squad_stats(competition, year, data_type):

    try:
        import pandas as pd
        import check_comp
        import requests
        from bs4 import BeautifulSoup

        comp = check_comp.check_comp(competition)
        season = f"{str(year)}-{str(year+1)}"
        url = f"https://fbref.com/en/comps/{comp[0]}/{season}/{data_type}/{season}-{comp[1]}-Stats"

        resp = requests.get(url) 
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text.replace('<!--', '').replace('--!>', ''), 'html.parser')

        headers, team_names, rows = [], [], []

        table_data = soup.find_all('tbody')[0]
        table_rows = table_data.find_all('tr')

        for value in table_rows[0]:
            headers.append(value.get('data-stat'))

        for row in table_rows:
            team_name = row.a.get_text()
            team_names.append(team_name)

        for row in table_rows:
            row_values = []
            row_data = row.find_all('td')
            for data_value in row_data:
                row_values.append(data_value.get_text())
            rows.append(row_values)

        df = pd.DataFrame(rows)
        df.insert(0, "team", team_names)
        df.columns = headers

        return df
    except: print("Invalid data input")

def opponent_stats(competition, year, data_type):

    try:
        import pandas as pd
        from internal_packages import check_comp
        import requests
        from bs4 import BeautifulSoup

        comp = check_comp.check_comp(competition)
        season = f"{str(year)}-{str(year+1)}"
        url = f"https://fbref.com/en/comps/{comp[0]}/{season}/{data_type}/{season}-{comp[1]}-Stats"

        resp = requests.get(url) 
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text.replace('<!--', '').replace('--!>', ''), 'html.parser')

        headers, team_names, rows = [], [], []

        table_data = soup.find_all('tbody')[1]
        table_rows = table_data.find_all('tr')

        for value in table_rows[0]:
            headers.append(value.get('data-stat'))

        for row in table_rows:
            team_name = row.a.get_text()
            team_names.append(team_name)

        for row in table_rows:
            row_values = []
            row_data = row.find_all('td')
            for data_value in row_data:
                row_values.append(data_value.get_text())
            rows.append(row_values)

        df = pd.DataFrame(rows)
        df.insert(0, "team", team_names)
        df.columns = headers

        return df
    except: print("Invalid data input")