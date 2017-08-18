def print_all(list):
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
all_sprints = []

sprint_num = re.compile("^Sprint ([0-9]+)")
num_rows = sheet.nrows
current_row = 4

while current_row < num_rows:
    single = []
    single.append(sheet.cell(current_row, TYPE).value)
    # single.append(sheet.cell(current_row, KEY).value)
    sprints = sheet.cell(current_row, SPRINT).value.split(", ")
    single.append(sprints)

    for sprint in sprints:
        sprint_number = sprint_num.findall(sprint)

        if len(sprint_number) >= 1:
            all_sprints.append(sprint_number[0])

    all_issues.append(single)
    current_row = current_row + 1

print_all(all_issues)
# print_all(all_sprints)

