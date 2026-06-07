import json
import os
import random
import sys
import urllib.error
import urllib.request

_TODOIST_TASKS_URL = "https://api.todoist.com/rest/v2/tasks"


def _fetch_open_tasks(token: str) -> list[str]:
    req = urllib.request.Request(
        _TODOIST_TASKS_URL,
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req) as resp:
        payload = json.load(resp)
    return [task["content"] for task in payload]


def perform_choose(n: int) -> None:
    if n <= 0:
        print("choose how many? n must be at least 1.", file=sys.stderr)
        raise SystemExit(2)

    token = os.environ.get("TODOIST_API_TOKEN")
    if not token:
        print(
            "TODOIST_API_TOKEN is not set. Get a token at "
            "Todoist → Settings → Integrations → Developer, "
            "then export it in your shell.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    try:
        tasks = _fetch_open_tasks(token)
    except urllib.error.HTTPError as e:
        print(f"Todoist API error: {e.code} {e.reason}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as e:
        print(f"could not reach Todoist: {e.reason}", file=sys.stderr)
        raise SystemExit(1)

    if not tasks:
        print("no open tasks to choose from.")
        return

    chosen = random.sample(tasks, min(n, len(tasks)))

    print("chosen are:")
    for task in chosen:
        print(f"  - {task}")
    print("Godspeed.")
