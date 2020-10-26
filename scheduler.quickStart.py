#from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# imports below from tutorial
import pandas as pd
import json
import csv
from google.oauth2 import service_account
import pygsheets
import instructor
import session

# If modifying these scopes, delete the file token.pickle.
#SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
# URL to gerald.depasquale spreadsheet https://docs.google.com/spreadsheets/d/1i-pCWoeI6QMYFRPZ4R-iiy9_afYAk5RPCVw6deJ9sxs/edit?usp=sharing
# URL to stafford https://docs.google.com/spreadsheets/d/1w_IhRW7DLulGYYqoBfX7C7dqNfeW1mGtt_FrHAE2KWY/edit?usp=sharing
# URL to stafford https://docs.google.com/spreadsheets/d/1l5H7K8PBBJjls06oKUQGyg9iCnOShzCU_ewwhqxrTds/edit?usp=sharing
# URL to Development Work Availability Form  https://docs.google.com/spreadsheets/d/1M4XgwiMZpuKglxUF0LV76_Si8fV7YvNI6PBPqod_dls/edit?usp=sharing
# URL to Student Master Schedule https://docs.google.com/spreadsheets/d/11Dd2lnHgdMINFVBO-1sOyacnyZBsEeaE9Ruz_9Mrcfc/edit?usp=sharing
SPREADSHEET_ID_1 = '1M4XgwiMZpuKglxUF0LV76_Si8fV7YvNI6PBPqod_dls'
SPREADSHEET_ID_2 = '11Dd2lnHgdMINFVBO-1sOyacnyZBsEeaE9Ruz_9Mrcfc'
RANGE_NAME = 'A1:E'
SPREADSHEET_NAME_1 = 'Mathnasium Work Availability Form (Responses)'
SPREADSHEET_NAME_2 = 'Master Student Schedule (Version 6).20200910'
INSTRUCTOR_SHEET_NAME = 'Form Responses 1'
EXPECTED_STUDENTS_SHEET_NAME = 'Expected Students'
SECRET_FILE = 'C:\PythonPrograms\SchedulerGSheets\Working Directory\credentials.json'
SESSION_RANGE = 'A2:Q9'



def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    # creds = None
    # # The file token.pickle stores the user's access and refresh tokens, and is
    # # created automatically when the authorization flow completes for the first
    # # time.
    # if os.path.exists('token.pickle'):
    #     with open('token.pickle', 'rb') as token:
    #         creds = pickle.load(token)
    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             SECRET_FILE, SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('token.pickle', 'wb') as token:
    #         pickle.dump(creds, token)
    #
    # service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    # sheet = service.spreadsheets()
    # result = sheet.values().get(spreadsheetId=SPREADSHEET_ID_1,
    #                             range=RANGE_NAME).execute()
    # values = result.get('values', [])
    #
    # if not values:
    #     print('No data found.')
    # else:
    #     print('Column A, Column E:')
    #     for row in values:
    #         # Print columns A and E, which correspond to indices 0 and 4.
    #         print('%s, %s' % (row[0], row[4]))
# From here forward, using pygsheets ...
    client = pygsheets.authorize(client_secret=SECRET_FILE)
#    master_schedule = client.sheet.get(SPREADSHEET_ID_2)
#    master_schedule = client.open(SPREADSHEET_NAME_2)
#    expected_students_sheet = master_schedule.worksheet_by_title(WKS_EXPECTED_STUDENTS_NAME)
#    print(expected_students_sheet)
#    bSheet = client.sheet.get(SPREADSHEET_ID_1)
    bSheet = client.open(SPREADSHEET_NAME_1)
    instructor_sheet = bSheet.worksheet_by_title(INSTRUCTOR_SHEET_NAME)
    instructors = []
    for i in instructor_sheet:
        instructors.append(instructor.Instructor(i))
    instructors.pop(0) #delete instructor created from the header row
#    [i.print() for i in instructors]
#     print("Instructors who can work at Stafford at 3 pm on Monday")
#     for i in instructors:
#         if i.can_work_location("Stafford") and i.can_work_session("Monday","3 pm"):
#             i.print()
#     print("Instructors who can work at Chancellor at 3 pm on Monday")
#     for i in instructors:
#         if i.can_work_location("Chancellor") and i.can_work_session("Monday","3 pm"):
#             i.print()
#     print("Instructors who can work at Home at 3 pm on Monday")
#     for i in instructors:
#         if i.can_work_location("Home") and i.can_work_session("Monday", "3 pm"):
#             i.print()

#    master_schedule = client.sheet.get(SPREADSHEET_ID_2)
    master_schedule = client.open(SPREADSHEET_NAME_2)
    expected_students_sheet = master_schedule.worksheet_by_title(EXPECTED_STUDENTS_SHEET_NAME)
    print("Monday Sessions:")

    print(expected_students_sheet.get_value('B3'), expected_students_sheet.get_value('A4'), expected_students_sheet.get_value('B4'))
    print(expected_students_sheet.get_value('B3'), expected_students_sheet.get_value('A5'), expected_students_sheet.get_value('B5'))
    print(expected_students_sheet.get_value('B3'), expected_students_sheet.get_value('A6'), expected_students_sheet.get_value('B6'))
    print(expected_students_sheet.get_value('B3'), expected_students_sheet.get_value('A7'), expected_students_sheet.get_value('B7'))
    print(expected_students_sheet.get_value('B3'), expected_students_sheet.get_value('A8'), expected_students_sheet.get_value('B8'))
    print(expected_students_sheet.get_value('B3'), expected_students_sheet.get_value('A9'), expected_students_sheet.get_value('B9'))
#    sessions = []
#    for i in expected_students_sheet:
#        sessions.append(session.Session(i))
 #       instructors.pop(0)  # delete instructor created from the header row
#    [i.print() for i in sessions]


if __name__ == '__main__':
    main()