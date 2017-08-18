import numpy as np
import matplotlib.pyplot as plt
import xlrd
import re

def print_all(list):
    for issue in list:
        print(issue)

TYPE = 0
SPRINT = 3
EPIC = 4

# get JIRA excel sheet
book = xlrd.open_workbook("JIRA_Stories.xlsx")
# get the first worksheet
sheet = book.sheet_by_index(0)

all_sprints = []
string_sprints = []
integer_sprints = []


# set the number of rows to analyze
num_rows = sheet.nrows
current_row = 4

# analyze JIRA excel sheet
while current_row < num_rows:
    single = []
    single.append(sheet.cell(current_row, TYPE).value)
    single.append(sheet.cell(current_row, EPIC).value)
    # in a single row, find the sprints that the issue was worked on (if any)
    sprints = sheet.cell(current_row, SPRINT).value
    if len(sprints) == 0:
        string_sprints.append("Not Used")
        current_row += 1
        continue
    else:
        sprints = sprints.split(", ")

    for sprint in sprints:
        if "Sprint" not in sprint:
            string_sprints.append(sprint)
            continue
        sprint_number = re.findall(r"^Sprint ([0-9]+)", sprint)
        if sprint_number:
            integer_sprints.append(int(sprint_number[0]))

    current_row += 1

# combine all sprints into one list
integer_sprints = sorted(integer_sprints)
string_sprints = sorted(string_sprints)
for sprint_number in integer_sprints:
    all_sprints.append("Sprint " + str(sprint_number))
for sprint in string_sprints:
    all_sprints.append(sprint)

stories_per_sprint = {}

# count the number of stories per sprint
for sprint in all_sprints:
    if sprint not in stories_per_sprint.keys():
        stories_per_sprint[sprint] = 0
    stories_per_sprint[sprint] += 1

for k, v in stories_per_sprint.items():
    print(k, v)