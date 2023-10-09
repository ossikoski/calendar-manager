class Game:
    def __init__(self, round, weekday, date, time, home, away, place, additional):
        self.round = round
        self.weekday = weekday
        self.date = date
        self.time = time
        self.home = home
        self.away = away
        self.place = place
        self.additional = ''
        if additional != None:
            self.additional = additional