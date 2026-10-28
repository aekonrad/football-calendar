import requests

URLS = [
    "https://ics.ecal.com/ecal-sub/6ae101eeab3d250002be7fee/English%20Premier%20League.ics",
    "https://ics.ecal.com/ecal-sub/6ae10179a360e100024c4264/Liverpool%20FC.ics",
    "https://ics.ecal.com/ecal-sub/6ae1025ea360e100024c4268/The%20FA.ics"
]

events_seen = set()
calendar_header = None
calendar_footer = "END:VCALENDAR\n"
all_events = []

for url in URLS:
    print(f"Downloading {url}")

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.text

    if calendar_header is None:
        calendar_header = data.split("BEGIN:VEVENT")[0]

    parts = data.split("BEGIN:VEVENT")

    for event_part in parts[1:]:
        event = "BEGIN:VEVENT" + event_part

        summary = ""
        dtstart = ""

        for line in event.splitlines():
            if line.startswith("SUMMARY"):
                summary = line.strip().lower()

            if line.startswith("DTSTART"):
                dtstart = line.strip()

        key = (summary, dtstart)

        if key not in events_seen:
            events_seen.add(key)
            all_events.append(event)

with open("football.ics", "w", encoding="utf-8") as f:
    f.write(calendar_header)

    for event in all_events:
        f.write(event)
        if not event.endswith("\n"):
            f.write("\n")

   
