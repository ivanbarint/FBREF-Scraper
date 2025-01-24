def check_comp(comp):
    output = ""
    if comp.lower() == 'england' or comp.lower() == "premier league" or comp.lower() == "eng":
        league_code = 9
        league_name = "Premier-League"
    elif comp.lower() == 'spain' or comp.lower() == "la liga" or comp.lower() == "esp":
        league_code = 12
        league_name = "La-Liga"
    elif comp.lower() == 'italy' or comp.lower() == "serie a" or comp.lower() == "ita":
        league_code = 11
        league_name = "Serie-A"
    elif comp.lower() == 'germany' or comp.lower() == "bundesliga" or comp.lower() == "ger":
        league_code = 20
        league_name = "Bundesliga"
    elif comp.lower() == 'france' or comp.lower() == "ligue 1" or comp.lower() == "fra":
        league_code = 13
        league_name = "Ligue-1"
    return league_code, league_name