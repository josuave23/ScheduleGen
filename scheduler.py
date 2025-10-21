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
from  datetime import date, timedelta
from math import ceil, floor


CHUNK_SIZE = 15

class Task():
    def __init__(self, name, due, work_minutes, priority=1, desc="", min_chunk_minutes=None):
        """
        Represents a schedulable task.

        Parameters:
            name (str): Task name.
            due (datetime.date): Due date for the task.
            work_minutes (int): Total minutes required to complete the task.
            priority (int): Importance level (higher = more important).
            desc (str): Optional description of the task.
            min_chunk_minutes (int): Minimum time per work chunk (default: 15 min).
        """
        self.name = name
        self.desc = desc
        self.due = due
        self.remaining = ceil(work_minutes / CHUNK_SIZE)
        self.priority = max(1, priority)
        self.min_chunk = ceil((min_chunk_minutes or CHUNK_SIZE) / CHUNK_SIZE)

    def __repr__(self):
        return (
            f"{self.name}(rem={self.remaining}, due={self.due}, "
            f"p={self.priority}, desc='{self.desc[:20]}...')"
        )
    
class Calendar:
    def __init__(self):
        self.tasks = []

    def addTask(self, title, desc, year=None, month=None, day=None, wTime=None):
        dueDate = None
        if year and month and day:
            try:
                dueDate = datetime.date(year, month, day)
            except ValueError:
                print("Invalid date provided")
                return
        task = Task(title, desc, dueDate, wTime)
        self.tasks.append(task)
        print(f"Task '{desc}' added")

    def viewTasks(self, date=None):
        for task in self.tasks:
            if date is not None:
                if task.due == date:
                    print(task)
            else:
                print(task)

    def removeTask(self, name):
        for task in self.tasks:
            if task.name == name:
                self.tasks.remove(task)

    # def updateTask(self, name):
    #     # UPDATE: Add a try catch statement to make this more robust
    #     nDate = input("Enter the new due date in MM-DD-YYYY format: ")
    #     dateStrings = nDate.split("-")


def generateSchedule(tasks, start, availableMinutes, lastDay=None):



# calendar = Calendar()
# calendar.addTask("helo", "work")
# calendar.viewTasks()


# def sortByPriority():



# def main():
#     calendar = Calendar()
#     calendar.addTask("test")
# main()
