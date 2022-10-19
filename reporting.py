from contextlib import contextmanager
from time import time
import requests
session = requests.session()

url = "http://localhost:9014"

def post_status(step, state, duration=None):
  try:
    status = {"step":step, "state":state}
    if duration is not None: status["duration"] = duration
    if url is not None:
        session.post(f"{url}/state", json=status)
  except Exception:
    print("Failed to send status", status)
    pass

def post_progress(operation, current, total):
  try:
    status = {"operation": operation, "current": current, "total": total}
    if url is not None:
        session.post(f"{url}/progress", json=status)
  except Exception:
    print("Failed to send status", status)
    pass

@contextmanager
def state(step):
    post_status(step, "start")
    start = time()

    try:
        yield
    except Exception as error:
        print(f"[{step}] errored:", error)
        post_status(step, "error", error=error)

    duration = time() - start
    post_status(step, "done", duration=duration)