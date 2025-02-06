def get_basic_position(style):
    
    print(style)

    splitted = style.split('(')
    width = float(splitted[2].split('%')[0])
    height = float(splitted[1].split('%')[0])
    
    group = ""
    
    if width < 10:
        group = "GK"
    elif width < 20:
        group = "DF"
    elif width < 40:
        group = "MF"
    else:
        group = "FW"
  
    return group

def get_detailed_position(style, gk, df, mf, fw):
    
    splitted = style.split('(')
    width = float(splitted[2].split('%')[0])
    height = float(splitted[1].split('%')[0])
    
    print(width)
    print(height)
    
    right_position = ""
    
    if width < 10:
        position = "GK"
    elif width < 20:
        if df > 3:
            if height < 20 or height > 80:
                position = "WB"
            else:
                position = "CB"
        else:
            position = "CB"
    elif width == 25:
        if height < 20 or height > 80:
            position = "WB"
        else:
            position = "DM"
    elif width == 30:
        if mf == 3:
            position = "CM"
        else:
            if height < 20 or height > 80:
                position = "WM"
            else:
                position = "CM"
    elif width == 35:
        if height == 50:
            position = "AM"
        else:
            position = "WF"
    else:
        if height < 20 or height > 80:
            position = "WF"
        else:
            position = "ST"
    
    return position