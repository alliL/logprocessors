def print_issues(list):
    for issue in list:
        print(issue)

import xlrd
import re

TYPE = 0
KEY = 1
SPRINT = 3

book = xlrd.open_workbook("C:/Users/awslee/PycharmProjects/August2017/JIRA_Sprints.xlsx")
# get the first worksheet
sheet = book.sheet_by_index(0)

all_issues = []

num_rows = sheet.nrows
current_row = 4

while current_row < num_rows:
    single = []
    single.append(sheet.cell(current_row, TYPE).value)
    # single.append(sheet.cell(current_row, KEY).value)
    single.append(sheet.cell(current_row, SPRINT).value.split(", "))

    all_issues.append(single)
    current_row = current_row + 1

print_issues(all_issues)


# Convert Date and Time: https://stackoverflow.com/questions/26010455/convert-xldate-to-python-datetime
# Read Excel Sheet: https://www.blog.pythonlibrary.org/2014/04/30/reading-excel-spreadsheets-with-python-and-xlrd/
# Module: http://www.lexicon.net/sjmachin/xlrd.html#xlrd.xldate_as_tuple-function
