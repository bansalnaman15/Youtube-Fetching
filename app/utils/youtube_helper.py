from datetime import datetime, timedelta
from croniter import croniter


class YoutubeHelper:
    def fetch_data(self, search_key, cron_schedule):
        print(datetime.now(), "Fetching data now!", search_key, "Schedule:", cron_schedule)

        now = datetime.now()
        iter = croniter(cron_schedule, now)
        last_run = iter.get_prev(datetime)
        print(f"Fetching data for '{search_key}' since '{last_run}'")
        pass

    def save_data(self, data):
        pass
