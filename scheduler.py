"""
This class generates the Schedule. (possibly an object):
Schedule will be based on the amount of minutes in a day, but used in 15 minute chunks

IDEAS:
    - minimum time on task per chunk

RULES:
    - Task should be able to be complete by due date, regardless of priority
    - Tasks with higher priority should be given more time

    

START:
    - Ask user for number of minutes in a day they can work
    - Ask user for minimum time on task per chunk
    - Get all tasks from event and
    - Sort tasks by due date
    - Create a list of days, each day is a list of 15 minute chunks
    - For each task, starting with the highest priority, fill in the chunks with the task until the work time is met or the due date is reached
    - If the task cannot be completed by the due date, move on to the next task
    - If there are any remaining chunks in a day, leave them empty
    - Return the schedule


"""

# import event
# import transcriber

# import calendar
# import tkinter

# class testCalendar(calendar.Calendar):
#     def formatMonth(self, year, month):
#         dates = self.monthdatescalendar(year, month)
    


# def main():
#     pass
# main()
import datetime

class Task():
    def __init__(self, dueDate, desc, workTime=0, priority=0):
        self.due = dueDate  #string
        self.desc = desc  #string
        self.w= workTime  # int
        self.p = priority  #int
        self.c = False  #Bool (completion)

    def __str__(self):
        status = "Waiting"
        if self.completed:
            status = "Done"
        date_str = f" (Due: {self.due.strftime('%Y-%m-%d')})" if self.due else ""
        return f"{status} {self.desc}{date_str}"
    
class Calendar:
    def __init__(self):
        self.tasks = []

    def addTask(self, desc, year=None, month=None, day=None, wTime=None):
        dueDate = None
        if year and month and day:
            try:
                dueDate = datetime.date(year, month, day)
            except ValueError:
                print("Invalid date provided")
                return
        task = Task(dueDate, desc, wTime)
        self.tasks.append(task)
        print(f"Task '{desc}' added")

    def viewTasks(self, date=None):
        