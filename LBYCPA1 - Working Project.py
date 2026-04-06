import time
import sys
import json
from datetime import datetime

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

    while seconds >= 0:
        timer_display = format_time(seconds)
        sys.stdout.write(f"\rTime Remaining [{label}]: {timer_display} ")
        sys.stdout.flush()
        time.sleep(1)
        seconds -= 1
    print(f"\n{label} session complete!")

def run_smart_timer(p_score):
    mode_name, work_mins, break_mins = get_urgency_mode(p_score)

    print(f"\n" + "=" * 40)
    print(f"URGENCY ALERT: {mode_name}")
    print(f"Panic Score: {p_score:.2f}")
    print("=" * 40)

    countdown_clock(work_mins, label="FOCUS")

    print("\a")  # System beep
    print("\nPROMPT: Take a break. Step away from the screen.")

    countdown_clock(break_mins, label="BREAK")

    print("\n" + "=" * 40)
    print("Session Finished! Ready for another?")
    print("=" * 40)

def calculate_remaining_hours(deadline):
    try:
        deadline_time = datetime.strptime(deadline, "%m/%d/%Y %I:%M:%S %p")
        current_time = datetime.now()

        remaining_time = deadline_time - current_time
        return remaining_time.total_seconds() / 3600

    except ValueError:
        return None

def store_data():
    while True:
        task_name = input('\nEnter name of Task: ')
        est_hours = float(input('Enter the Estimated Hours to Complete: '))

        print('\nEnter Deadline in the format MM/DD/YYYY HH:MM:SS AM/PM')
        print(f'For Example: {datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")}\n')
        deadline = input('Enter Deadline: ')
        remaining_hours = calculate_remaining_hours(deadline)

        if remaining_hours is None:
            print('\nPlease make sure the date matches the format MM/DD/YYYY HH:MM:SS AM/PM\n')
            continue

        panic_score = calculate_panic_score(est_hours, remaining_hours)

        all_tasks[task_name] = {
            "Estimated Hours": est_hours,
            "Remaining Hours": remaining_hours,
            "Deadline": deadline,
            "Panic Score": panic_score
        }

        print(f'Task "{task_name}" has been saved!')

        repeat = input('\nAdd another task? (Y/N): ')
        if repeat.upper() == 'N':
            break

def start_task():
    while True:

        input_start_task = input('\nChoose a Task to Start: ')

        if input_start_task in all_tasks:
            start_now = input("Start the timer for this task now? (Y/N): ")

            if start_now.upper() == 'Y':
                panic_score = all_tasks[input_start_task]['Panic Score']
                run_smart_timer(panic_score)
            elif start_now.upper() == 'N':
                break

        else:
            print('Task not Found!')

all_tasks = {}

if __name__ == "__main__":

    while True:

        for task_name in all_tasks:
            panic_score = all_tasks[task_name]['Panic Score']
            print(f'{task_name} - Panic Score: {panic_score:.2f}')

        option = input("""
        1 - Enter Tasks
        2 - Start a Task
        0 - Exit
        Input Option: """)

        match option:
            case "1":
                store_data()

            case "2":
                start_task()

            case "0":
                print("Exiting Program...")
                break

            case _:
                print("Invalid Input!")

SAVE_FILE = "smart_tasks.json"

def save_data(data):

    try:
        with open(SAVE_FILE, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"File updated: {SAVE_FILE}")
    except Exception as e:
        print(f"An error occurred while saving: {e}")