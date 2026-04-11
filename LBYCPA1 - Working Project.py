import time
import sys
import json
from datetime import datetime

# ------------ Initializations ------------

SAVE_FILE = "smart_tasks.json"
data = {
    "Tasks": {},
    "Total Tasks": 0,
    "Completed Tasks": 0
}

# ------------ Data Files ------------

def save_data():
    try:
        with open(SAVE_FILE, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"File updated: {SAVE_FILE}")
    except Exception as e:
        print(f"An error occurred while saving: {e}")

def load_data():
    global data
    try:
        with open(SAVE_FILE, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"Tasks": {}, 
                "Total Tasks": 0, 
                "Completed Tasks": 0
        }

# ------------ Sub Functions ------------

def calculate_panic_score(est_hours, remaining_hours):
    try:
        return est_hours / remaining_hours
    except ZeroDivisionError:
        return float('inf')

def get_urgency_mode(p_score):
    if p_score < 0.25:
        return "Easy Mode", 25, 5
    elif 0.25 <= p_score < 0.8:
        return "Classic Mode", 35, 8
    elif 0.8 <= p_score < 1.0:
        return "Deep Focus", 50, 10
    else:
        return "Sprint Mode (Red Light Warning!)", 90, 10

def format_time(seconds):
    mins, secs = divmod(seconds, 60)
    return f"{mins:02d}:{secs:02d}"

def countdown_clock(minutes, label="Work"):
    seconds = minutes * 60
    print(f"\n--- {label} Session Started ---")
    print("Press Ctrl+C at any time to mark as COMPLETE or STOP.")

    try:
        while seconds >= 0:
            timer_display = format_time(seconds)
            sys.stdout.write(f"\rTime Remaining [{label}]: {timer_display} ")
            sys.stdout.flush()
            time.sleep(1)
            seconds -= 1
        print(f"\n{label} session complete!")
        return True
    except KeyboardInterrupt:
        print(f"\n\nTimer stopped by user.")
        return False

def run_smart_timer(p_score):
    mode_name, work_mins, break_mins = get_urgency_mode(p_score)

    print(f"\n" + "=" * 40)
    print(f"URGENCY ALERT: {mode_name}")
    print("=" * 40)

    completed_early = not countdown_clock(work_mins, label="FOCUS")

    if completed_early:
        return

    print("\a\nPROMPT: Take a break.")
    countdown_clock(break_mins, label="BREAK")
    return

def calculate_remaining_hours(deadline):
    try:
        deadline_time = datetime.strptime(deadline, "%m/%d/%Y %I:%M %p")
        current_time = datetime.now()

        remaining_time = deadline_time - current_time
        hours = remaining_time.total_seconds() / 3600
        return max(hours, 0)

    except ValueError:
        return None
    
def update_panic_score():
    for task_name in data['Tasks']:
        deadline = data['Tasks'][task_name]['Deadline']
        remaining_hours = calculate_remaining_hours(deadline)
        est_hours = data['Tasks'][task_name]['Estimated Hours']
        data['Tasks'][task_name]['Panic Score']= calculate_panic_score(est_hours, remaining_hours)

def progressBar(finishedTasks, totalTasks):
    try:
        percentageTasks = (finishedTasks / totalTasks) * 100 
        Bar = '|' + '█' * int(percentageTasks/2) + '-' * int((100 - percentageTasks)/2) + '|'
        return f'\nPercentage: {percentageTasks}%\nProgress Bar:\n{Bar}'
    except ZeroDivisionError:
        percentageTasks = 1
        Bar = '|' + '█' * int(percentageTasks/2) + '-' * int((100 - percentageTasks)/2) + '|'
        return f'\nYou have no active tasks!\n\nProgress Bar:\n{Bar}'

# ------------ User Action ------------

def store_data():
    while True:
        task_name = input('\nEnter name of Task: ')
        est_hours = float(input('Enter the Estimated Hours to Complete: '))

        print('\nEnter Deadline in the format MM/DD/YYYY HH:MM AM/PM')
        print(f'For Example: {datetime.now().strftime("%m/%d/%Y %I:%M %p")}\n')
        
        while True:
            deadline = input('Enter Deadline: ')
            remaining_hours = calculate_remaining_hours(deadline)

            if remaining_hours is None:
                print('Please make sure the date matches the format MM/DD/YYYY HH:MM:SS AM/PM\n')
            
            else:
                break

        panic_score = calculate_panic_score(est_hours, remaining_hours)

        data["Tasks"][task_name] = {
            "Estimated Hours": est_hours,
            "Remaining Hours": remaining_hours,
            "Deadline": deadline,
            "Panic Score": panic_score,
        }

        data['Total Tasks'] += 1
        print(f'Task "{task_name}" has been saved!')
        save_data()

        repeat = input('\nAdd another task? (Y/N): ')
        if repeat.upper() == 'N':
            break

def start_task():
    while True:
        if not data['Tasks']:
            print("There are no tasks yet!")
            break

        input_start_task = input('\nChoose a Task to Start: ')

        selected_task = None
        for task_name in data['Tasks']:
            if task_name.upper() == input_start_task.upper():
                selected_task = task_name
                break

        if selected_task:
            start_now = input('Start the timer for this task now? (Y/N): ')

            if start_now.upper() == 'Y':
                panic_score = data['Tasks'][selected_task]['Panic Score']

                run_smart_timer(panic_score)

                complete = input('Type "Complete" to finish and remove the task, or press Enter to keep it: ')
                if complete.upper() == 'COMPLETE':
                    del data['Tasks'][selected_task]
                    data['Completed Tasks'] += 1
                    save_data()
     
                break

            elif start_now.upper() == 'N':
                break

        else:
            print('Task not Found!')    


if __name__ == "__main__":

    load_data()

    while True:

        update_panic_score()

        print(progressBar(data['Completed Tasks'], data['Total Tasks']))

        sorted_tasks = sorted(data['Tasks'].items(), key=lambda x: x[1]['Panic Score'], reverse=True)

        for task_name, task_data in sorted_tasks:
            panic_score = task_data['Panic Score']
            print(f'{task_name} - Panic Score: {panic_score:.2f}')
        
        option = input("""
        1 - Enter Tasks
        2 - Start a Task
        3 - Reset Progress Bar
        4 - Clear Data
        0 - Exit
        Input Option: """)

        match option:
            case "1":
                store_data()

            case "2":
                start_task()

            case "3":
                data['Total Tasks'] = len(data['Tasks'])
                data['Completed Tasks'] = 0
                save_data()

            case "4":
                confirm = input("Confirm by Y/N: ")
                if confirm.upper() == 'Y':
                    data = {
                        "Tasks": {},
                        "Total Tasks": 0,
                        "Completed Tasks": 0
                    }
                    save_data()

            case "0":
                save_data()
                print('Exiting Program...')
                break

            case _:
                print('Invalid Input!')