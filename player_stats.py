## Creating the url and returning fetched dataframe

def seasonal_player_data(competition, year, data_type):
    
    import pandas as pd
    from internal_packages import check_comp, fetch_player_data
    import requests
    from bs4 import BeautifulSoup
    
    try:
        comp = check_comp.check_comp(competition) ## Checking competitions with pre-created formula
        season = f"{str(year)}-{str(year+1)}" ## Creating proper season string
        url = f"https://fbref.com/en/comps/{comp[0]}/{season}/{data_type}/{season}-{comp[1]}-Stats" ## Creating the url
        df = fetch_player_data.fetch_seasonal_player_data(url) ## Fetching data

        return df ## Returning dataframe if all inputs are proper
    except: return "Invalid data input" ## Returning string what shows invalid input