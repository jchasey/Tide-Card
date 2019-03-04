#!/usr/bin/python3

import json
import bs4 as bs
import urllib.request
import time
import datetime as dt

url = 'https://www.ntslf.org/tides/tidepred?port=Newlyn'

html = urllib.request.urlopen(url).read()
soup = bs.BeautifulSoup(html, 'html.parser')

# Select the tide table and the elements therein containing the times & heights
tides = soup.find(id="ntslf-tide-table").find_all("span")
tide_data = {}
peak_times = []
peak_heights = []

# Is first tide of the day low or high?
if (tides[2].contents[0][-1] == "L"):
    tide_data['FirstHighTide'] = tides[3].contents[0]
else:
    tide_data['FirstHighTide'] = tides[1].contents[0]

# Get initial date stripping tags
datestr = tides[0].contents[0].get_text()
# Convert th, rd or st to whitespace
datestr = datestr.replace("st"," ")
datestr = datestr.replace("nd"," ")
datestr = datestr.replace("rd"," ")
datestr = datestr.replace("th"," ")
date = dt.datetime.strptime(datestr,"%a %d %b %Y")

t = 1;
lasthours = 0;
while t < 18:
    # Make sure field has data & ignore non-times
    if tides[t].contents:
        # Debug print (t,' - ',tides[t].contents)

        if tides[t].contents[0][0].isdigit():
            timestr = tides[t].contents[0].split(':')
            hours = int(timestr[0])
            mins = int(timestr[1])

            # Increment day if needed
            if (hours < lasthours):
                date += dt.timedelta(days=1)
            lasthours = hours

            # Set hours and mins of the tide
            date = date.replace(hour=hours,minute=mins)

            peak_times.append(date)
            peak_heights.append(float(tides[t+1].contents[0][:-3].strip()))

            t += 2
        else:
            # The next day field
            t += 1

tide_data['PeakTimes'] = peak_times
tide_data['PeakHeights'] = peak_heights

json = json.dumps(tide_data, indent=4, sort_keys=True, default=str)
print (json)
