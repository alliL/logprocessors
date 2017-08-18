# Python35

import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import collections
import xlrd
import re

plotly.tools.set_credentials_file(username='alliL', api_key='5sBi7Oz6wAAKzenByJSZ')
plotly.tools.set_config_file(world_readable=True, sharing='public')

def print_all(list):
    for issue in list:
        print(issue)

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
            all_sprints.append(int(sprint_number[0]))

    all_issues.append(single)
    current_row = current_row + 1

x_axis = []
y_axis = []
y_axis_data = {}

all_sprints = sorted(all_sprints)

# create x and y axis labels
for sprint_num in all_sprints:
    sprint_num_string = "Sprint " + str(sprint_num)
    if sprint_num_string not in x_axis:
        x_axis.append(sprint_num_string)
        y_axis_data[sprint_num] = 0
    y_axis_data[sprint_num] = y_axis_data[sprint_num] + 1

y_axis_data = y_axis_data.values()
for value in y_axis_data:
    y_axis.append(value)

data = [go.Bar(
            x=x_axis,
            y=y_axis
    )]

py.plot(data, filename='Sprints')
