import unittest
from unittest import mock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from gui.main import CFlowGUI

class TestCFlowGUI(unittest.TestCase):
    def setUp(self):
        self.root = mock.MagicMock()
        self.root.after = lambda delay, func: func()
        self.gui = CFlowGUI(master=self.root, cli_path='echo')

    @mock.patch('subprocess.run')
    @mock.patch('gui.main.threading.Thread')
    def test_run_command_success(self, mock_thread, mock_run):
        process_mock = mock.Mock(stdout='ok', stderr='')
        mock_run.return_value = process_mock

        class DummyThread:
            def __init__(self, target, args=(), daemon=None):
                self.target = target
                self.args = args

            def start(self):
                self.target(*self.args)

        mock_thread.side_effect = DummyThread

        self.gui.command_entry.get = mock.Mock(return_value='--version')
        self.gui.output = mock.Mock()
        self.gui.run_command()

        mock_run.assert_called()
        self.gui.output.delete.assert_called_once()
        self.gui.output.insert.assert_any_call('end', 'ok')

    @mock.patch('subprocess.run', side_effect=FileNotFoundError)
    @mock.patch('gui.main.threading.Thread')
    def test_run_command_missing_cli(self, mock_thread, mock_run):
        class DummyThread:
            def __init__(self, target, args=(), daemon=None):
                self.target = target
                self.args = args
            def start(self):
                self.target(*self.args)

        mock_thread.side_effect = DummyThread

        self.gui.command_entry.get = mock.Mock(return_value='--help')
        self.gui.output = mock.Mock()
        with mock.patch('tkinter.messagebox.showerror') as mbox:
            self.gui.run_command()
            mbox.assert_called_once()

    @mock.patch('subprocess.run')
    @mock.patch('gui.main.threading.Thread')
    def test_run_command_with_stderr(self, mock_thread, mock_run):
        process_mock = mock.Mock(stdout='out', stderr='oops')
        mock_run.return_value = process_mock

        class DummyThread:
            def __init__(self, target, args=(), daemon=None):
                self.target = target
                self.args = args
            def start(self):
                self.target(*self.args)

        mock_thread.side_effect = DummyThread

        self.gui.command_entry.get = mock.Mock(return_value='--bad')
        self.gui.output = mock.Mock()
        self.gui.run_command()
        self.gui.output.insert.assert_any_call('end', 'out\n[stderr]\noops')

    @mock.patch('gui.main.threading.Thread')
    def test_run_command_empty(self, mock_thread):
        class DummyThread:
            def __init__(self, target, args=(), daemon=None):
                self.target = target
                self.args = args
            def start(self):
                self.target(*self.args)

        mock_thread.side_effect = DummyThread

        self.gui.command_entry.get = mock.Mock(return_value='')
        self.gui.output = mock.Mock()
        with mock.patch('tkinter.messagebox.showwarning') as warn:
            self.gui.run_command()
            warn.assert_called_once()
