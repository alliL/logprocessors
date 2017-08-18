def print_issues(list):
    for issue in list:
        print(issue)

import xlrd
import re

TYPE = 0
KEY = 1
UPDATE_DATE = 9

book = xlrd.open_workbook("C:/Users/awslee/PycharmProjects/August2017/JIRA_Tests.xlsx")
# get the first worksheet
sheet = book.sheet_by_index(0)

all_issues = []
quarter_one = []
quarter_two = []
quarter_three = []
quarter_four = []

num_rows = sheet.nrows
current_row = 4

date = re.compile("([0-9-]+) ")
Q1 = re.compile("-(04|05|06)-")
Q2 = re.compile("-(07|08|09)-")
Q3 = re.compile("-(10|11|12)-")
Q4 = re.compile("-(01|02|03)-")

while current_row < num_rows:
    single = []
    single.append(sheet.cell(current_row, TYPE).value)
    single.append(sheet.cell(current_row, KEY).value)
    date_time = xlrd.xldate.xldate_as_datetime(sheet.cell(current_row, UPDATE_DATE).value, book.datemode)
    py_date = date.findall(str(date_time))
    single.append(py_date[0])

    if Q1.findall(str(date_time)):
        quarter_one.append(single)
    elif Q2.findall(str(date_time)):
        quarter_two.append(single)
    elif Q3.findall(str(date_time)):
        quarter_three.append(single)
    elif Q4.findall(str(date_time)):
        quarter_four.append(single)

    all_issues.append(single)
    current_row = current_row + 1


#print_issues(all_issues)
print_issues(quarter_one)
#print_issues(quarter_two)
#print_issues(quarter_three)
#print_issues(quarter_four)

# Convert Date and Time: https://stackoverflow.com/questions/26010455/convert-xldate-to-python-datetime
# Read Excel Sheet: https://www.blog.pythonlibrary.org/2014/04/30/reading-excel-spreadsheets-with-python-and-xlrd/
# Module: http://www.lexicon.net/sjmachin/xlrd.html#xlrd.xldate_as_tuple-function
