from __future__ import print_function
import os.path
from ast import literal_eval

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from basket_scraper import get_basket_schedule

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar'] #.readonly


def main():
    """
    Add events in to calendar based on web scraper.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Get schedule from men's 1. division A games by Raholan Pyrkivä:
    # Link is hard coded for season 2023-24
    schedule_dict = get_basket_schedule('https://www.basket.fi/basket/sarjat/joukkue/?team_id=4600311&season_id=127056&league_id=2')
    # Parse results and add events for each game:
    for round, game in schedule_dict.items():
        if game.home == 'Raholan Pyrkivä':
            summary = f'vs. {game.away}'
        if game.away == 'Raholan Pyrkivä':
            summary = f'@ {game.home}'

        month = game.date.split('.')[1]
        if month[0] == '0':  # Remove zero from month
            month = month[1:]
        year = 2023
        if literal_eval(month) < 7:
            year = 2024
        if len(month) < 2:  # Add the zero back to month :D
            month = f'0{month}'
        day = game.date.split('.')[0]
        if len(day) < 2:  # Add the zero to day
            day = f'0{day}'
        end_hour = literal_eval(game.time.split(':')[0]) + 2
        end_minute = game.time.split(':')[-1]
        
        # All colorIds: https://lukeboyle.com/blog/posts/google-calendar-api-color-id
        event = {
            'summary': summary,
            'location': game.place,
            'description': f'Round {game.round}. {game.additional}',
            'start': {
                'dateTime': f'{year}-{month}-{day}T{game.time}:00+02:00',
                'timeZone': 'Europe/Helsinki',
            },
            'end': {
                'dateTime': f'{year}-{month}-{day}T{end_hour}:{end_minute}:00+02:00',
                'timeZone': 'Europe/Helsinki',
            },
            'colorId': 7
        }
        
        # Call the Calendar API
        event = service.events().insert(calendarId='primary', body=event).execute()  # TODO Uncomment
        print('Event created: %s' % (event.get('htmlLink')))

if __name__ == '__main__':
    main()
    