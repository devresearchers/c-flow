"""Simple Tkinter GUI wrapper around ``claude-flow`` CLI."""

import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import shlex
import threading
from pathlib import Path

class CFlowGUI:
    """Tkinter-based interface for running ``claude-flow`` commands."""

    def __init__(self, master=None, cli_path: str | None = None):
        self.master = master or tk.Tk()
        self.master.title('C‑Flow GUI')

        default = Path(__file__).resolve().parent.parent / 'bin' / 'claude-flow'
        env_path = os.environ.get('CFLOW_CLI_PATH')
        self.cli_path = Path(cli_path or env_path or default)

        self._build_widgets()

    def _build_widgets(self):
        frm = ttk.Frame(self.master, padding=10)
        frm.grid(row=0, column=0, sticky='nsew')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.command_entry = ttk.Entry(frm, width=50)
        self.command_entry.grid(row=0, column=0, sticky='ew')
        frm.columnconfigure(0, weight=1)
        run_btn = ttk.Button(frm, text='Run', command=self.run_command)
        run_btn.grid(row=0, column=1, padx=5)

        self.output = scrolledtext.ScrolledText(frm, width=80, height=20)
        self.output.grid(row=1, column=0, columnspan=2, pady=10, sticky='nsew')
        frm.rowconfigure(1, weight=1)

    def run_command(self):
        """Validate input and spawn a thread to execute the command."""
        cmd = self.command_entry.get().strip()
        if not cmd:
            messagebox.showwarning('Warning', 'Please enter a command.')
            return

        full_cmd = [str(self.cli_path), *shlex.split(cmd)]
        thread = threading.Thread(target=self._execute_command, args=(full_cmd,), daemon=True)
        thread.start()

    def _execute_command(self, full_cmd: list[str]):
        """Run the subprocess and update the GUI when finished."""
        try:
            completed = subprocess.run(full_cmd, capture_output=True, text=True, check=False)
        except FileNotFoundError:
            self.master.after(0, lambda: messagebox.showerror('Error', f'CLI not found at {self.cli_path}'))
            return

        output = completed.stdout
        if completed.stderr:
            output += '\n[stderr]\n' + completed.stderr

        def update():
            self.output.delete('1.0', tk.END)
            self.output.insert(tk.END, output)

        self.master.after(0, update)

    def run(self):  # pragma: no cover - simple Tk main loop
        self.master.mainloop()

if __name__ == '__main__':  # pragma: no cover - manual entry point
    gui = CFlowGUI()
    gui.run()
