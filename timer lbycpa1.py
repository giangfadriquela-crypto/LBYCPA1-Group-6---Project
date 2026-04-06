import time
import sys

def format_time(seconds):
    mins, secs = divmod(seconds, 60)
    return f"{mins:02d}:{secs:02d}"

def countdown_clock(minutes, label="Work"):
    # Convert minutes to seconds for the loop
    seconds = minutes * 60
    
    print(f"\n--- {label} Session Started ---")
    
    while seconds >= 0:
        # The \r allows us to overwrite the same line in the terminal
        timer_display = format_time(seconds)
        sys.stdout.write(f"\rTime Remaining [{label}]: {timer_display} ")
        sys.stdout.flush()
        
        time.sleep(1)
        seconds -= 1
    
    print(f"\n{label} session complete!")

def run_smart_timer(p_score):
    # 1. Determine the mode based on your existing logic
    mode_name, work_mins, break_mins = get_urgency_mode(p_score)
    
    print(f"\n" + "="*40)
    print(f"URGENCY ALERT: {mode_name}")
    print(f"Panic Score: {p_score:.2f}")
    print("="*40)

    # 2. Run the Work Cycle
    countdown_clock(work_mins, label="FOCUS")
    
    # 3. Alert the user (using a simple print or \a for a bell sound)
    print("\a") # System beep
    print("\nPROMPT: Take a break. Step away from the screen.")
    
    # 4. Run the Break Cycle
    countdown_clock(break_mins, label="BREAK")
    
    print("\n" + "="*40)
    print("Session Finished! Ready for another?")
    print("="*40)