import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Import the start_app module
import start_app

class TestMacLogic(unittest.TestCase):
    
    @patch('platform.system')
    @patch('subprocess.Popen')
    def test_start_server_macos(self, mock_popen, mock_system):
        """Test that start_server generates the correct AppleScript on macOS."""
        print("\nTesting macOS start_server logic...")
        
        # 1. Simulate being on macOS
        mock_system.return_value = "Darwin"
        
        # 2. Call the function with dummy data
        test_name = "Test Server"
        test_cmd = "python run.py"
        test_cwd = "/Users/test/project"
        
        start_app.start_server(test_name, test_cmd, test_cwd)
        
        # 3. Verify subprocess.Popen was called
        self.assertTrue(mock_popen.called, "subprocess.Popen should be called")
        
        # 4. Inspect the arguments passed to Popen
        args, _ = mock_popen.call_args
        command_list = args[0]
        
        # Check if it tries to run 'osascript' (AppleScript runner)
        self.assertEqual(command_list[0], "osascript", "Should use osascript on macOS")
        
        # Check the actual script content
        script_content = command_list[2]
        print(f"Generated AppleScript:\n{script_content}")
        
        self.assertIn('tell application "Terminal"', script_content)
        # Note: The script escapes quotes, so we look for escaped versions
        # The code does: safe_cwd = cwd.replace('"', '\\"')
        # And puts it in: "cd \\"{safe_cwd}\\"
        # So we expect: cd \"/Users/test/project\"
        self.assertIn(f'cd \\"{test_cwd}\\"', script_content)
        self.assertIn(test_cmd, script_content)
        print("✅ start_server logic for macOS is correct.")

    @patch('platform.system')
    @patch('subprocess.Popen')
    @patch('shutil.which')
    def test_start_server_linux(self, mock_which, mock_popen, mock_system):
        """Test that start_server finds a terminal on Linux."""
        print("\nTesting Linux start_server logic...")
        
        # 1. Simulate Linux
        mock_system.return_value = "Linux"
        
        # 2. Simulate 'gnome-terminal' being available
        def side_effect(arg):
            if arg == 'gnome-terminal':
                return '/usr/bin/gnome-terminal'
            return None
        mock_which.side_effect = side_effect
        
        start_app.start_server("Test Linux", "python run.py", "/tmp")
        
        # 3. Verify it tried to launch gnome-terminal
        self.assertTrue(mock_popen.called)
        args, _ = mock_popen.call_args
        cmd_list = args[0]
        self.assertEqual(cmd_list[0], "gnome-terminal")
        print("✅ start_server logic for Linux is correct.")

    @patch('platform.system')
    @patch('shutil.which')
    @patch('subprocess.run')
    def test_kill_port_macos(self, mock_run, mock_which, mock_system):
        """Test that kill_port uses lsof on macOS."""
        print("\nTesting macOS kill_port logic...")
        
        # 1. Simulate macOS
        mock_system.return_value = "Darwin"
        
        # 2. Simulate 'lsof' being installed
        mock_which.return_value = "/usr/bin/lsof"
        
        # 3. Simulate lsof finding a process (PID 12345)
        # The first call to run is the check, return a PID
        mock_run.return_value.stdout = "12345"
        
        start_app.kill_port(5000)
        
        # 4. Verify the kill command was constructed
        kill_called = False
        for call in mock_run.call_args_list:
            args, kwargs = call
            if len(args) > 0 and isinstance(args[0], str) and "kill -9" in args[0]:
                print(f"Detected kill command: {args[0]}")
                kill_called = True
        
        self.assertTrue(kill_called, "Should attempt to run 'kill -9' via lsof on macOS")
        print("✅ kill_port logic for macOS is correct.")

if __name__ == '__main__':
    unittest.main()
