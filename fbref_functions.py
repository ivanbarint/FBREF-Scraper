def player_seasonal_stats():
    comp = input("Enter competition: ")
    season = int(input("Enter season: "))
    data_type = input("Enter data type: ")
    
    from internal_packages import player_stats
    df = player_stats.player_stats(comp, season, data_type)
    
    return df

def player_full_seasonal_stats():
    comp = input("Enter competition: ")
    season = int(input("Enter season: "))
    
    from internal_packages import player_stats
    df = player_stats.full_player_stats(comp, season)
    
    return df

def keeper_full_seasonal_stats():
    comp = input("Enter competition: ")
    season = int(input("Enter season: "))
    
    from internal_packages import player_stats
    df = player_stats.full_keeper_stats(comp, season)
    
    return df

def team_seasonal_stats():
    comp = input("Enter competition: ")
    season = int(input("Enter season: "))
    data_type = input("Enter data type: ")
    
    from internal_packages import team_stats
    df = team_stats.squad_stats(comp, season, data_type)
    
    return df

def team_seasonal_opp_stats():
    comp = input("Enter competition: ")
    season = int(input("Enter season: "))
    data_type = input("Enter data type: ")
    
    from internal_packages import team_stats
    df = team_stats.opponent_stats(comp, season, data_type)
    
    return df

def results_and_fixtures():
    comp = input("Enter competition: ")
    season = int(input("Enter season: "))
    
    from internal_packages import scores_and_fixtures
    df = scores_and_fixtures.season_results_and_fixtures(comp, season)

    return df