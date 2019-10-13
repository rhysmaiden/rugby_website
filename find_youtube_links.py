#Run script every 3 hours

import wikipedia
import os
import subprocess
import youtube_videos
import time
import datetime
from youtube_videos import youtube_search
from datetime import datetime, timedelta
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
import django
django.setup()

from rugby.models import Match



matches = Match.objects.filter(video_link_found=0)

print(len(matches))



for match in matches:

    start_time_period = match.date
    end_time_period = match.date + timedelta(days=5)

    print(end_time_period)



    found_videos = youtube_search(match.home_team.team_name + " v " + match.away_team.team_name + " rugby highlights")
    foundVideo = False
    video_id = ""

    for video in found_videos:

        video_date = datetime.strptime(video.date[:10],"%Y-%m-%d")
        if  video_date > start_time_period and video_date < end_time_period:
            video_id = video.video_id
            foundVideo = True
            break

    if foundVideo:
        match.video_link_found = 1
        match.video_link = "https://www.youtube.com/watch?v=" + video_id

        print("Found: " + str(match))
        match.save()
    else:
        print("Didn't Find: " + str(match))
