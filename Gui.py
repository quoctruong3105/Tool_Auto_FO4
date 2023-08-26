import tkinter as tk
import subprocess

class AutoFO4Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoFO4 Interface")

        self.start_button = tk.Button(root, text="Start Automation", command=self.start_automation)
        self.stop_button = tk.Button(root, text="Stop Automation", command=self.stop_automation)

        self.start_button.pack()
        self.stop_button.pack()

        self.is_running = False
        self.script_process = None

    def start_automation(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.script_process = subprocess.Popen(["python", "AutoFO4.py"])
            self.script_process.communicate()

    def stop_automation(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            if self.script_process:
                self.script_process.terminate()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoFO4Interface(root)
    root.mainloop()
