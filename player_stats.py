## Creating the url and returning fetched dataframe

def player_stats(competition, year, data_type):
    
    import pandas as pd
    from internal_packages import check_comp
    import requests
    from bs4 import BeautifulSoup
    
    try:
        comp = check_comp.check_comp(competition) ## Checking competitions with pre-created formula
        season = f"{str(year)}-{str(year+1)}" ## Creating proper season string
        url = f"https://fbref.com/en/comps/{comp[0]}/{season}/{data_type}/{season}-{comp[1]}-Stats" ## Creating the url

        resp = requests.get(url) 
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text.replace('<!--', '').replace('--!>', ''), 'html.parser')

        ## Creting two lists which will be filled with data
        
        headers, rows = [], []
        
        ## Getting values from the very first row of the table, from which with iterration we will get all the values from 'data-stat' attributes, which will be used as headers

        table_data = soup.find_all('tbody')[2]
        table_rows = table_data.find_all('tr')

        ## Getting the headers and putting them into the headers list
        
        for value in table_rows[0]:
            headers.append(value.get('data-stat'))
            
        ## Getting every row value and putting them into the rows list

        for row in table_rows:
            row_values = []
            row_data = row.find_all('td')
            for data_value in row_data:
                if data_value.get('data-append-csv'):
                    row_values.append(data_value.get('data-append-csv')) ## 'data-append-csv' is an attribute inside of each row representing the unique code for every player, which will be used as 'player_id' later
                row_values.append(data_value.get_text())
            rows.append(row_values)
            
        ## Creating the dataframe

        df = pd.DataFrame(rows, columns = headers).fillna(0) ## Creating the dataframe from the data
        df = df.loc[df['player'] != 0].reset_index(drop = True) ## FBRef has an unused row every approx 25 rows which is filled with NaN. This code is to remove it, while immediately reseting the index to ease further iterrations

        ## Minutes are displayed with a comma where the values go over one thousand, so we need to remove ',' from the string, to later convert the value into numerical
        
        if 'minutes' in headers:
            df['minutes'] = df['minutes'].str.replace(',', '')
        elif 'gk_minutes' in headers:
            df['gk_minutes'] = df['gk_minutes'].str.replace(',', '')

        ## For the actual season, age column always shows the age in format yy-ddd, with the players age exactly shown in years and days
        ## Following algorithm is used to remove dash and ddd, so data can be transformed into numerical value
        
        for i, row in df.iterrows():
            try:
                if '-' in row['age']: ## If '-' exist in the column
                    age_num = row['age'].split('-')[0] ## Splitting the string where the '-' is and keeping only the part before it (years of age), storing it into an age_num variable
                    df.at[i, 'age'] = age_num ## Changing values in every row where column is age with the age_num variable
            except Exception: pass ## Ignoring if data transformation is not necessary

        df.rename(columns={'ranker' : 'player_id'}, inplace=True) ## Renaming the first column from ranker to player_id for easier understading
        df = df.apply(pd.to_numeric, errors = 'ignore') ## Transforming all possible values from object into numerical values, ignoring the ones that cannot be changed instead of deleting or changing them

        return df ## Returning dataframe if all inputs are proper
    except: return "Invalid data input" ## Returning string what shows invalid input