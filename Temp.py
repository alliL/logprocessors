import xlrd
import re

issues = {}
dates = []
key = []
this_year = {}
date = re.compile("([0-9-]+) ")

book = xlrd.open_workbook("C:/Users/awslee/PycharmProjects/August2017/JIRA_Tests.xlsx")
# get the first worksheet
sheet = book.sheet_by_index(0)

for cell in sheet.col_slice(colx=8, start_rowx=4):
    # print(cell)
    py_date = xlrd.xldate.xldate_as_datetime(cell.value, book.datemode)
    py_date = date.findall(str(py_date))
    dates.append(py_date[0])

for cell in sheet.col_slice(colx=1, start_rowx=4):
    key.append(cell.value)

for i in range(0, len(key)):
    issues[dates[i]] = key[i]

for k, v in issues.items():
    print(k + ", " + v)
    if k[:4] == '2017':
        this_year[k] = v
print(this_year)


# Convert Date and Time: https://stackoverflow.com/questions/26010455/convert-xldate-to-python-datetime
# Read Excel Sheet: https://www.blog.pythonlibrary.org/2014/04/30/reading-excel-spreadsheets-with-python-and-xlrd/
# Module: http://www.lexicon.net/sjmachin/xlrd.html#xlrd.xldate_as_tuple-function