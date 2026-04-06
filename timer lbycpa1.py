import time
import sys


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

def store_data():
    while True:
        task_name = input('\nEnter name of Task: ')
        est_hours = float(input('Enter the Estimated Hours to Complete: '))
        remaining_hours = float(input('Enter Hours remaining until Deadline: '))

        panic_score = calculate_panic_score(est_hours, remaining_hours)

        all_tasks[task_name] = {
            "Estimated Hours": est_hours,
            "Remaining Hours": remaining_hours,
            "Panic Score": panic_score
        }

        print(f'Task "{task_name}" has been saved!')

        start_now = input("Start the timer for this task now? (Y/N): ")
        if start_now.upper() == 'Y':
            run_smart_timer(panic_score)

        repeat = input('\nAdd another task? (Y/N): ')
        if repeat.upper() == 'N':
            break

all_tasks = {}

if __name__ == "__main__":
    store_data()
    print("\nFinal Task Summary:")
    print(all_tasks)
