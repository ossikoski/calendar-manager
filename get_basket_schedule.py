from PyPDF2 import PdfFileReader


SCHEDULE_PATH = './schedule_files/m1db_sarjaohjelma_21-22.pdf'

class Game:
    def __init__(self, round, day, date, time, home, away, place, additional):
        self.round = round
        self.day = day
        self.date = date
        self.time = time
        self.home = home
        self.away = away
        self.place = place
        if additional != None:
            self.additional = additional


def get_basket_schedule(team, schedule_path):
    """
    Get the schedule of the wanted team from a pdf file given.

    Returns
    -------
        schedule : dict of Game objects with round number as key.
    """
    with open(schedule_path, 'rb') as schedule_file:
        pdf = PdfFileReader(schedule_file)

        schedule_dict = dict()
        for page_num in range(pdf.getNumPages()):
            page = pdf.getPage(page_num)
            text = page.extractText()

            # Regular season:
            text = text.split('\nKierros ')
            for i, row in enumerate(text):
                if 'MIESTEN I DIVISIOONA B' in row:  # Header row
                    continue
                
                if '1. putoamisve' in row:  # Last row
                    cells = row.split('\n1. putoamisve')[0].split('\n')
                else:
                    cells = row.split('\n')
                
                home = cells[3].replace('•', 'Ä').replace('ı', 'ö').replace('−', 'ä')
                away = cells[4][1:].replace('•', 'Ä').replace('ı', 'ö').replace('−', 'ä')
                if team == home or team == away:
                    # Additional info on the game
                    additional = None
                    try:
                        additional = cells[7]
                    except IndexError:
                        pass
                    
                    game = Game(cells[0], cells[1][:2], cells[1][2:], cells[2], home, away, cells[5], additional)
                    schedule_dict[cells[0]] = game

    return schedule_dict

schedule = get_basket_schedule('Raholan Pyrkivä', SCHEDULE_PATH)
