import sys
import json
import urllib.request
import urllib.error





def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"

    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Python-CLI-App"})

        with urllib.request.urlopen(request) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                display_activity(data)
            else:
                print(f"Error: {response.status} - {response.reason}")

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("User not found.")
        else:
            print(f"Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"Error: {e.reason}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def display_activity(data):
    if not data:
        print("No activity found.")
        return

    print("GitHub Activity:")
    for event in data:
        event_type = event.get("type")
        repo_name = event.get("repo", {}).get("name")

        if event_type == "PushEvent":
            commit_count = len(event.get("payload", {}).get("commits", []))
            print(f"- Pushed {commit_count} commit(s) to {repo_name}")
        elif event_type == "IssuesEvent":
            action = event.get("payload", {}).get("action")
            print(f"- {action.capitalize()} an issue in {repo_name}")
        elif event_type == "WatchEvent":
            print(f"- Starred {repo_name}")
        elif event_type == "CreateEvent":
            ref_type = event.get("payload", {}).get("ref_type")
            print(f"- Created a {ref_type} in {repo_name}")
        else:
            print(f"- {event_type.replace('Event', '')} in {repo_name}")


if __name__ == "__main__":
    username = sys.argv[1]

    if len(sys.argv) < 2 :
        print("Usage: python github_activity.py <username>")
        sys.exit(1)

    fetch_github_activity(username)