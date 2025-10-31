import random


def generateTaskFromUtilization(UtilizationSet, ImplicitDeadline):
    taskList = []
    for i in range(len(UtilizationSet)):
        p = random.randint(2, 10)
        e = p * UtilizationSet[i]

        if ImplicitDeadline:
            d = p
        else:
            # alpha = random.uniform(0.1, 0.9)
            alpha = 0.60
            d = (1 - alpha) * p + alpha * e
            
        taskList.append(task(p, e, d))
    return taskList


def writeTaskSetToFile(TaskSetID, taskSetList, file):
    # append to file here
    file.write("Task Set : " + str(TaskSetID))
    file.write("\n")
    for i in range(len(taskSetList)):
        file.write( str(taskSetList[i].getExecutionTime()) + " " +
                    str(taskSetList[i].Period()) + " " +
                    str(taskSetList[i].RelativeDeadline()) + "\n")


class task(object):
    def __init__(self, p, e, d):
        self.period = p
        self.executionTime = e
        self.deadline = d
        self.seen = False
        self.ID = -1
        self.executedTime = 0
        self.cycle = 1

    def Period(self):
        return self.period

    def getExecutionTime(self):
        return self.executionTime

    def getExecutedTime(self):
        return self.executedTime

    def Utilization(self):
        return (self.executionTime)/(self.period)

    def RelativeDeadline(self):
        return self.deadline

    def getSeenFlag(self):
        return self.seen

    def seenFlagActivation(self):
        self.seen = True
        return True

    def setID(self, ID):
        self.ID = ID

    def getID(self):
        return self.ID

    def reset(self):
        self.seen = False
        self.cycle += 1
        self.executedTime = 0

    # it's automatically activate seen flag
    def execute(self, currentTime):
        self.executedTime = self.executedTime + 1
        if(self.executedTime == self.executionTime):
            self.seenFlagActivation()
        # if(currentTime > self.period):
        #     return False
        # else:
        #     return True
