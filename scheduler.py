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


NOTES:
- Implement the Blackout feature
    - Also implement a way to give breaks at regular intervals
- check whether dailyAmount is working properly
- make a more intuitive list format    
    
"""



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


def generateSchedule(tasks, start, availableMinutes, lastDay=None):\
    #LOGIC FIX-------(Maybe)----------------------------------------------------
    #dailyAmount is being treated as the entire available time for the whole week
    #I should change that to either be the daily amount available or to be the whole week
    if lastDay is None:
        lastDay = max(t.due for t in tasks)

    #finding available time
    dailyAmount = floor(availableMinutes / CHUNK_SIZE)
    if dailyAmount <= 0:
        return {}, ["Not enough available time (<15 minutes)"]
    
    #feasible check

    warnings = []
    sortedTasks = sorted(tasks, key=lambda t: t.due)
    for t in sortedTasks:
        remainingTime = 0
        current = start
        while current <= t.due:
            remainingTime += dailyAmount
            current += timedelta(days=1)
        requiredTime = sum(x.remaining for x in sortedTasks if x.due <= t.due)
        if requiredTime > remainingTime:
            warnings.append(
                f"Infeasible by {t.due}: need {requiredTime*CHUNK_SIZE} minutes, "
                f"capacity {remainingTime*CHUNK_SIZE} minutes (shortfall {(requiredTime - remainingTime)*CHUNK_SIZE} minutes)"
            )
            break

    schedule = {}
    current = start

    while current <= lastDay:
        dailyPlan = []
        timeRemaining = dailyAmount

        eligible = [t for t in tasks if t.remaining > 0 and t.due >= start]

        required = {}
        for t in eligible:
            daysLeft = max(1, (t.due - current).days + 1)
            neededToday = ceil(t.remaining / daysLeft)
            take = min(neededToday, t.remaining, timeRemaining)

            if take > 0 and take < t.min_chunk and timeRemaining >= t.min_chunk and t.remaining >= t.min_chunk:
                take = t.min_chunk
            if take > 0:
                required[t] = take
                remainingTime -= take

        for t, take in required.items():
            t.remaining -= take
            dailyPlan.append((t.name, take))

        if timeRemaining > 0:
            elig2 = [t for t in tasks if t.remaining > 0 and t.due >= current]
            
            if elig2:
                weights = []
                for t in elig2:
                    daysLeft = max(1, (t.due - current).days + 1)
                    urgency = 1.0 / daysLeft
                    weights.append((t, t.priority * urgency))
                totalW = sum(w for _, w in weights) or 1.0

                while timeRemaining > 0 and any(t.remaining > 0 for t in elig2):
                    t = max((t for t, w in weights if t.remaining > 0), key=lambda x: next(w for tt, w in weights if tt is x))
                    take = min(max(1, t.min_chunk), t.remaining, timeRemaining)
                    take = min(take, timeRemaining)
                    
                    if take <= 0:
                        break
                    t.remaining -= take
                    timeRemaining -= take
                    dailyPlan.append((t.name, take))

        merged = []
        for name, chunks in dailyPlan:
            if merged and merged[-1][0] == name:
                merged[-1] = (name, merged[-1][1] + chunks)
            else:
                merged.append((name, chunks))
        schedule[current] = merged

        current += timedelta(days=1)
    return schedule, warnings


def main():
    tasks = []
    #blackout time has not been implemented yet
    blackout = input("How much break time do you want each day? (enter in minutes): ")
    totalTime = input("Enter how much time you want to work per day (enter in minutes): ")
    newTask = input("Please enter your first task to do (Name, YYYY-MM-DD, time in minutes, priority): ")
    while newTask != "0":
        hold = newTask.split(",")
        dateList = hold[1].split("-")
        tasks.append(Task(hold[0], date(int(dateList[0]), int(dateList[1]), int(dateList[2])), int(hold[2]), int(hold[3])))
        newTask = input("Enter another task (type 0 to finish): ")
    
    schedule, warnings = generateSchedule(
    tasks=tasks,
    start=date.today(),
    availableMinutes = int(totalTime)
    )

    for w in warnings:
        print("Warning:", w)

    for day, plan in schedule.items():
        # print day and each block in 15-minute units
        slots = [f"{name} x {chunks*15}min" for name, chunks in plan]
        print(day, "->", ", ".join(slots) if slots else "FREE")

    


main()