import pandas as pd
import json
import csv
from google.oauth2 import service_account
import pygsheets


def main():
    with open('C:\PythonPrograms\SchedulerGSheets\Working Directory\credentials.json') as source:
        info = json.load(source)
    credentials = service_account.Credentials.from_service_account_info(info)
    # URL to Development Work Availability Form  https://docs.google.com/spreadsheets/d/1M4XgwiMZpuKglxUF0LV76_Si8fV7YvNI6PBPqod_dls/edit?usp=sharing

#    client = pygsheets.authorize(service_account_file='C:\PythonPrograms\SchedulerGSheets\Working Directory\credentials.json')

if __name__ == '__main__':
    main()