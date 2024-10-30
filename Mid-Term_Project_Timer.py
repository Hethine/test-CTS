import time  # Makes time function like real world time in python
import threading  # Makes the program able to run multiple pieces of code together
import tkinter as tk  # toolbox for GUI
import os  # Module to interact with the operating system

# Conditional import for winsound
if os.name == 'nt':  # 'nt' indicates a Windows system
    import winsound  # Windows specific sound module
else:
    winsound = None  # Don't do anything for non-windows

# Class that handles the Alarm
class AlarmTimer:
    def __init__(self, duration, update_callback):
        self.duration = duration  # Timer duration in seconds
        self.paused = False  # Functions for different buttons in UI
        self.remaining = duration
        self._timer_thread = None
        self._lock = threading.Lock()
        self._is_running = False
        self.update_callback = update_callback  # Callback to update the UI

    def _run_timer(self):
        while self.remaining > 0 and self._is_running:
            with self._lock:
                if not self.paused:
                    # Decrement the remaining time by 1 second
                    self.remaining -= 1

                    # Update the UI with the remaining time
                    self.update_callback(int(self.remaining))

            time.sleep(1)  # Wait for 1 second before the next decrement

        if self.remaining <= 0 and self._is_running:
            self.update_callback(0)  # Update UI when time's up
            self.play_beeps()  # Play beeps when time is up
            print("Time's up!")

    def play_beeps(self):
        if winsound:  # Check if winsound is available
            for _ in range(3):  # Makes it beep three times instead of just once
                winsound.Beep(1000, 500)  # Frequency and time sound plays for
        else:
            print("Beep sound not supported on this OS.")

    def start(self):
        if self._is_running:
            print("Timer is already running!")
            return
        self._is_running = True
        self._timer_thread = threading.Thread(target=self._run_timer)
        self._timer_thread.start()
        print(f"Timer started for {self.duration} seconds!")

    def pause(self):
        with self._lock:
            if not self._is_running:
                print("Timer is not running!")
                return
            if self.paused:
                print("Timer is already paused!")
            else:
                self.paused = True
                print("Timer paused.")

    def unpause(self):
        with self._lock:
            if not self._is_running:
                print("Timer is not running!")
                return
            if not self.paused:
                print("Timer is not paused!")
            else:
                self.paused = False
                print("Timer resumed.")

    def stop(self):
        with self._lock:
            if not self._is_running:
                print("Timer is not running!")
                return
            self._is_running = False
            self.remaining = self.duration
            self.update_callback(self.duration)  # Reset display
            print("Timer reset.")

# UI Class
class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Timer")

        # Labels and entries for hours, minutes, seconds
        self.time_label = tk.Label(root, text="Enter duration (hh:mm:ss):", font=("Helvetica", 16))
        self.time_label.pack(pady=10)

        self.hours_entry = tk.Entry(root, width=5, font=("Helvetica", 16))
        self.hours_entry.pack(side="left", padx=5)
        self.hours_entry.insert(0, "00")

        self.minutes_entry = tk.Entry(root, width=5, font=("Helvetica", 16))
        self.minutes_entry.pack(side="left", padx=5)
        self.minutes_entry.insert(0, "00")

        self.seconds_entry = tk.Entry(root, width=5, font=("Helvetica", 16))
        self.seconds_entry.pack(side="left", padx=5)
        self.seconds_entry.insert(0, "00")

        # Start button
        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(side="left", padx=10)

        # Pause button
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_timer)
        self.pause_button.pack(side="left", padx=10)

        # Unpause button
        self.unpause_button = tk.Button(root, text="Unpause", command=self.unpause_timer)
        self.unpause_button.pack(side="left", padx=10)

        # Reset button (formerly Stop button)
        self.reset_button = tk.Button(root, text="Reset", command=self.stop_timer)
        self.reset_button.pack(side="left", padx=10)

    def start_timer(self):
        try:
            hours = int(self.hours_entry.get())
            minutes = int(self.minutes_entry.get())
            seconds = int(self.seconds_entry.get())
            total_seconds = hours * 3600 + minutes * 60 + seconds
            
            # Initialize and start the timer
            self.timer = AlarmTimer(total_seconds, self.update_time_display)
            self.timer.start()
            self.update_time_display(total_seconds)

            # Disable start button after timer is started
            self.start_button.config(state=tk.DISABLED)
        except ValueError:
            self.update_time_display("Invalid input! Enter numbers.")

    def pause_timer(self):
        if hasattr(self, 'timer'):
            self.timer.pause()

    def unpause_timer(self):
        if hasattr(self, 'timer'):
            self.timer.unpause()

    def stop_timer(self):
        if hasattr(self, 'timer'):
            self.timer.stop()
            # Re-enable start button after stopping/resetting the timer
            self.start_button.config(state=tk.NORMAL)

    def update_time_display(self, remaining):
        if isinstance(remaining, int):
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            seconds = remaining % 60
            # Format the timer correctly without an extra colon
            if remaining > 0:
                self.time_label.config(text=f"Time remaining: {hours:02}:{minutes:02}:{seconds:02}")
            else:
                self.time_label.config(text="Time's up!")  # Show time's up message
        else:
            self.time_label.config(text=remaining)

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)  # Initialize without a specific duration
    root.mainloop()


