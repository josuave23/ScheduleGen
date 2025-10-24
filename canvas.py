# import requests



# #access_token = ""

# userClassURL = "https://csulb.instructure.com/courses/98459"

# insertIndx = userClassURL.find("/", 8) + 1

# userApiURL = userClassURL[ : insertIndx] + "api/v1/users/self/" + userClassURL[insertIndx : ]

# canvasURL = userApiURL + "/assignments"

# requestURL = canvasURL + "?access_token=" + access_token

# assignmentsInfo = requests.get(requestURL).json()


# for assignmentInfo in assignmentsInfo:
#     try:
#         print("Name: " + assignmentInfo["name"])
#         print("Points: " + str(assignmentInfo["points_possible"]))
#         print("Due: " + assignmentInfo["due_at"])
#     except TypeError:
#         print("No Due Date")

#     print("\n")
import os, requests
from dotenv import load_dotenv 

load_dotenv()  

def fetch_assignments(base_url: str, course_id: str, token: str):
    url = f"{base_url.rstrip('/')}/api/v1/courses/{course_id}/assignments"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"per_page": 100}
    items = []

    while url:
        r = requests.get(url, headers=headers, params=params if url.endswith("/assignments") else None, timeout=30)
        r.raise_for_status()
        items.extend(r.json())

        next_url = None
        link = r.headers.get("Link", "")
        for part in link.split(","):
            segs = part.split(";")
            if len(segs) >= 2 and 'rel="next"' in segs[1]:
                next_url = segs[0].strip().lstrip("<").rstrip(">")
                break
        url = next_url

    return items

def main():
    base_url = os.getenv("CANVAS_BASE_URL") or input("Canvas base URL (e.g. https://csulb.instructure.com): ").strip()
    token = os.getenv("CANVAS_ACCESS_TOKEN") or input("Your Canvas Access Token: ").strip()
    course_id = os.getenv("COURSE_ID") or input("Course ID (e.g. 98459): ").strip()

    assignments = fetch_assignments(base_url, course_id, token)

    for a in assignments:
        name = a.get("name", "Untitled")
        points = a.get("points_possible", "N/A")
        due = a.get("due_at") or "No Due Date"
        print(f"Name: {name}\nPoints: {points}\nDue: {due}\n")

if __name__ == "__main__":
    main()