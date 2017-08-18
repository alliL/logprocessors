# !/usr/bin/python

# process  log files
import os
import paramiko  # to connect to nexus and jenkins server
import io
import json
import sys
import subprocess

# handles plot
import numpy as np
import matplotlib.pyplot as plt

# run ./gitlog.sh
subprocess.call("gitlog.sh", shell=True)

# checks if git log file exists
if (os.path.isdir('./branchjson')) == False:
    sys.exit("Git log directory do not exist \
            ")
# IMAGE SIZE
Y = 8
X = 20

username = "baba"
password = ""

# server connection for jenkins
jenkinsserver = "USDVRLNX01"

# server connection for nexus
nexusserver = "USDVRLNX02"

# connect to jenkins server
jenkins = paramiko.SSHClient()
jenkins.set_missing_host_key_policy(paramiko.AutoAddPolicy())
jenkins.connect(jenkinsserver, username=username, password=password)

# connect to nexus server
nexus = paramiko.SSHClient()
nexus.set_missing_host_key_policy(paramiko.AutoAddPolicy())
nexus.connect(nexusserver, username=username, password=password)

# files and directory
cwd = os.getcwd()
directory = cwd

gitjsondir = 'branchjson'
logfile = directory + "/" + "logger.txt"
file = open((logfile + ".txt"), 'w')


# process git log
def gitlog(filename):
    Insertions = 0
    Deletions = 0
    Commits = 0

    with open(gitjsondir + "/" + filename, 'r') as file:
        jsonfile = json.load(file)
        # get each object in the json file
        for data in jsonfile:
            commit = data['commit']
            Commits += 1
            paths = data['paths']

            for path in paths:
                if path['insertions'] != '-':
                    Insertions += int(path['insertions'])
                if path['deletions'] != '-':
                    Deletions += int(path['deletions'])

    return Insertions, Deletions, Commits


# process nexus log
def nexuslog(filename):
    branch = "*" + filename.replace('.json', '') + "*"
    getSize = "find /opt/sonatype-work/nexus/storage/snapshots  -maxdepth 1 -name " + branch + " -exec du -ch {} + | grep total$"
    nexus_stdin, stdout, nexus_stderr = nexus.exec_command(getSize)
    size = stdout.readlines()

    Totalsize = 0

    # convert channelfile to number
    for line in size:
        Totalsize = line.replace('total', '')
    return Totalsize


# process jenkins log
def jenkinslog(filename):
    NumofSuccess = 0
    NumofFailure = 0
    Unknown = 0
    Exit_EnterState = 0

    branch = filename.replace('.json', '')
    getNextBuildNum = "cat /var/lib/jenkins/jobs/'EPC Multibranch Build'/branches/" + branch + "/nextBuildNumber"
    jenkins_stdin, stdout, jenkins_stderr = jenkins.exec_command(getNextBuildNum)
    output = ""
    NextBuildNum = stdout.readlines()
    buildNum = 0

    # convert channelfile to number
    for line in NextBuildNum:
        buildNum = (int(line) - 1)
    for i in range(1, (buildNum + 1)):
        cmd_to_execute = "cat /var/lib/jenkins/jobs/'EPC Multibranch Build'/branches/" + branch + "/builds/" + str(
            i) + "/log  | grep -in Finished | cut -d\   -f2 "
        ssh_stdin, stdout, ssh_stderr = jenkins.exec_command(cmd_to_execute)
        output = ""
        text = ""
        log = stdout.readlines()
        # convert channelfile to text
        for line in log:
            line = output + line
            if "SUCCESS" in line:
                NumofSuccess += 1
            elif "FAILURE" in line:
                NumofFailure += 1
            else:
                Exit_EnterState += 1

    Unknown = buildNum - (NumofSuccess + NumofFailure)
    return NumofSuccess, NumofFailure, Exit_EnterState, Unknown, buildNum, branch


# convert the sizes to bytes
def convert(val):
    val = str(val)
    if val == '0':
        return 0
    if 'G' in val:
        val = val.replace('G', '')
        val = (float(val) * 1000000000)
    elif 'M' in val:
        val = val.replace('M', '')
        val = (float(val) * 1000000)

    return int(val)


# write to a textfile and return a lists of log data
def fileWrite():
    branchname = []
    insertions = []
    commits = []
    success = []
    failure = []
    size = []
    deletions = []
    builds = []

    # loop through work streams
    for filename in os.listdir(gitjsondir):
        if filename.endswith(".json"):

            # jenkins
            NumofSuccess, NumofFailure, Exit_EnterState, Unknown, buildNum, branch = jenkinslog(filename)
            # nexus
            Totalsize = nexuslog(filename)
            # gitlog
            Insertions, Deletions, Commits = gitlog(filename)

            if Commits == 0 or buildNum == 0:
                continue
                # write to file
            Totalsize = convert(Totalsize)
            file.write((branch + "\n" + "Builds: " + str(buildNum) + "\n"))
            file.write(("Commits: " + str(Commits) + "\n"))
            file.write(("Insertions: " + str(Insertions) + "\n"))
            file.write(("Deletions: " + str(Deletions) + "\n"))
            file.write(("Success: " + str(NumofSuccess) + "\n"))
            file.write(("Failure: " + str(NumofFailure) + "\n"))
            # file.write(("Exit_EnterState: " +   str(Exit_EnterState)      + "\n"))
            file.write(("Unknown: " + str(Unknown) + "\n"))
            file.write(("Total_Size: " + str(Totalsize) + "\n"))
            # print ("Processing " + branch + "...")


            branchname.append(filename.replace('.json', ''))
            insertions.append(int(Insertions))
            deletions.append(int(Deletions))
            commits.append(int(Commits))
            success.append(int(NumofSuccess))
            failure.append(int(NumofFailure))
            size.append(Totalsize)
            builds.append(int(buildNum))

            break

    return branchname, insertions, deletions, commits, \
           success, failure, size, builds


# creat plots
def plot():
    branch, insertions, deletions, commits, success, failure, size, builds = fileWrite()
    IDC = zip(insertions, deletions, commits)
    SFB = zip(success, failure, builds)

    # bar charts
    # Size of Builds for Each Branch
    figure1 = uniBar(branch, size, 'Size_of_Builds_for_Each_Branch', 'Branch', 'Size in Bytes', 1000000)
    # Number of Builds for each branch
    figure2 = uniBar(branch, builds, 'Number_of Builds_for_each_branch', 'Branch', 'builds', 1)
    # number of commits for each branch
    figure3 = uniBar(branch, commits, 'Number_of_commits_for_each_branch', 'Branch', 'Commits ', 1)

    # Aggregate Plot of builds success and Failure
    fig4legend = ['Build', 'Failure', 'Success']
    figure4 = multiBar(branch, SFB, 'Aggregate_Plot_of_builds_success_and_Failure', 'Branch', 'y', fig4legend)
    ##Aggregate Plot of commits insertions and deletions
    fig5legend = ['Commits', 'Deletions', 'Insertions']
    figure5 = multiBar(branch, IDC, 'Aggregate_Plot_of_commits_insertions_and_deletions', 'Branch', 'y', fig5legend)

    # pieChart
    # plot of number of Builds for each branch
    figure6 = pieChart(branch, builds, "Number_of_Builds_for_Each_Branch")
    # percentage of commits for each branch
    figure7 = pieChart(branch, commits, "Percentage_of_commits_for_each_branch")


# plot  pie chart
def pieChart(label_list, x_list, title):
    fig, ax = plt.subplots()
    x = np.char.array(label_list)
    y = np.array(x_list)

    percent = (100. * y / y.sum())
    patches, texts = plt.pie(y, startangle=90, radius=1.0)
    labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(x, percent)]
    plt.title(title.replace("_", " "))
    sort_legend = True
    if sort_legend:
        patches, labels, dummy = zip(*sorted(zip(patches, labels, y),
                                             key=lambda x: x[2],
                                             reverse=True))
    plt.legend(patches, labels, loc='best', bbox_to_anchor=(-0.1, 1.),
               fontsize=8)

    plt.draw()
    fig.set_size_inches(X, Y)
    fig.savefig((title + "_piechart" + ".png"), bbox_inches='tight')


# multiple bar chat
# N = no of bars,x = x-axis,y- y-axis
def multiBar(x, y, title, xlabel, ylabel, legends):
    greenvals, redvals, bluevals = zip(*y)
    ind = np.arange(len(x))  # the x locations for the groups
    width = 0.27  # the width of the bars
    fig, ax = plt.subplots()

    green = ax.bar(ind, greenvals, width, color='g', label=legends[2])
    red = ax.bar(ind + width, redvals, width, color='r', label=legends[1])
    blue = ax.bar(ind + width * 2, bluevals, width, color='b', label=legends[0])

    # axes parameter
    ax.set_title(title.replace("_", " "))
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation='vertical')
    ax.autoscale(tight=True)

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * h, '%d' % int(h),
                    ha='center', va='bottom')

    autolabel(green)
    autolabel(red)
    autolabel(blue)

    plt.draw()
    ax.legend()
    fig.set_size_inches(X, Y)
    fig.savefig((title + "_barchart" + ".png"), bbox_inches='tight')


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


# main
def main():
    plot()
    nexus.close
    jenkins.close
    file.close()


if __name__ == '__main__':
    main()