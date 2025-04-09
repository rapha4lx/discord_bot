
from signal import Signals, signal
from asyncio import create_task
import subprocess

def setup_daemon(client):
    def handle_signal(signum, frame):
        if signum is Signals.SIGINT or Signals.SIGTERM:
            create_task(client.on_shutdown())
        elif signum is Signals.SIGHUP:
            create_task(client.on_restart())

    signal(Signals.SIGINT, handle_signal)
    signal(Signals.SIGTERM, handle_signal)
    signal(Signals.SIGHUP, handle_signal)

def check_for_changes(REMOTE_CHECK_NAME):
    try:
        # Fetch the latest changes from the remote repository
        subprocess.run(['git', 'fetch'], check=True)
        
        # Get the latest commit hash from the local main branch
        local_commit = subprocess.check_output(
            ['git', 'rev-parse', 'main']
        ).strip()
        
        # Get the latest commit hash from the remote main branch
        remote_commit = subprocess.check_output(
            ['git', 'rev-parse', REMOTE_CHECK_NAME]
        ).strip()
        
        if local_commit != remote_commit:
            subprocess.check_output(
                ['git', 'pull', 'origin', 'main'], check=True
            )
            exit(0)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while checking for changes: {e}")