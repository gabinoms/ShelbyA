async def gift_timer_info(sec):
    hours = [[1],[2,3,4],[5]]
    minutes = [[1],[2,3,4],[5,6,7,8,9,0]]
    eleven= [11,12,13,14]

    sec = 21600-sec
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    mint = sec // 60


    if hour in hours[0]:
        text_h='час'
    elif hour in hours[1]:
        text_h='часа'
    else:
        text_h='часов'

    if mint in minutes[2] or mint%10 in minutes[2] or mint in eleven:
        text_min='минут'
    elif mint in minutes[0] or mint%10 in minutes[0]:
        text_min='минуту'
    elif mint in minutes[1] or mint%10 in minutes[1]:
        text_min='минуты'

    return f'{hour} {text_h} {mint} {text_min}'



