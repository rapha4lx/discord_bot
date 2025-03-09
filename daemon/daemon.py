
from signal import Signals, signal
from asyncio import create_task

def setup_daemon(client):
    def handle_signal(signum, frame):
        if signum is Signals.SIGINT or Signals.SIGTERM:
            create_task(client.on_shutdown())
        elif signum is Signals.SIGHUP:
            create_task(client.on_restart())

    signal(Signals.SIGINT, handle_signal)
    signal(Signals.SIGTERM, handle_signal)
    signal(Signals.SIGHUP, handle_signal)