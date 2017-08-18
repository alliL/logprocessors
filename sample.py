import numpy as np
import matplotlib.pyplot as plt
import xlrd
import re

#IMAGE SIZE
Y = 8
X = 15

def print_all(list):
    for issue in list:
        print(issue)


# plot single barchart
# scale = width of label
def uniBar(a, b, title, xlabel, ylabel, scale):
    y, x = zip(*sorted((zip(b, a)), reverse=True))

    y_pos = np.arange(len(x))
    fig, ax = plt.subplots()
    w = 0.40

    sizerect = ax.bar(y_pos, y, width=w, color='r', align='center')
    ax.set_title(title.replace("_", " "))
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation='vertical')
    ax.autoscale(tight=True)

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.00 * h, '%d' % (int(h) / scale),
                    ha='center', va='bottom')

    autolabel(sizerect)
    plt.draw()
    fig.set_size_inches(X, Y)
    fig.savefig((title + "_barchart" + ".png"), bbox_inches='tight')

TYPE = 0
SPRINT = 3

# get JIRA excel sheet
book = xlrd.open_workbook("JIRA_Sprints.xlsx")
# get the first worksheet
sheet = book.sheet_by_index(0)

all_issues = []
all_sprints = []

# using regular expressions to search for Sprints
sprint_num = re.compile("^Sprint ([0-9]+)")

# set the number of rows to analyze
num_rows = sheet.nrows
current_row = 4

# analyze JIRA excel sheet
while current_row < num_rows:
    single = []
    single.append(sheet.cell(current_row, TYPE).value)
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

# create x and y axis data
for sprint_num in all_sprints:
    sprint_num_string = "Sprint " + str(sprint_num)
    if sprint_num_string not in x_axis:
        x_axis.append(sprint_num_string)
        y_axis_data[sprint_num] = 0
    y_axis_data[sprint_num] = y_axis_data[sprint_num] + 1

y_axis_data = y_axis_data.values()
for value in y_axis_data:
    y_axis.append(value)

# create graph
num_of_sprints_graph = uniBar(x_axis, y_axis, "Issues in Each Sprint", "Number of Sprints", "Number of Issues", 2)

# plot graph
plt.show(num_of_sprints_graph)