# Tide-Card
Lovelace Tide Card and script to retrieve tide levels

Before you can display the tide levels we need to retrieve the data. This script accesses the National Tidal and Sea Level Facility in the UK to grab the data.
The data is available for a number of locations around the UK, so it is a case of finding the closest station and adjusting the URL in the script.

For example:

`https://www.ntslf.org/tides/tidepred?port=Newlyn`

Will access the data for Newln in Cornwall, the full list of locations is at `https://www.ntslf.org/tides/predictions`. 

The script can just be run on the console and outputs the data in JSON format, for example:

```{
    "FirstHighTide": "01:50",
    "PeakHeights": [
        4.44,
        1.89,
        4.41,
        1.79,
        4.71,
        1.62,
        4.66,
        1.53
    ],
    "PeakTimes": [
        "2019-03-02 01:50:00",
        "2019-03-02 08:36:00",
        "2019-03-02 14:24:00",
        "2019-03-02 21:04:00",
        "2019-03-03 02:47:00",
        "2019-03-03 09:32:00",
        "2019-03-03 15:14:00",
        "2019-03-03 21:52:00"
    ]
}
```

The data is collected for the current day and tomorrow. Depending on the tide cycle this is usually 7 or 8 peak (either low or high) heights over the next 48 hours.

The next step is to get this data into Home Assistant, for which I use a command line sensor as follows:

```
sensor:
  - platform: command_line
    name: 'FirstHighTide'
    command: 'python3 /config/tide_scrape.py'
    scan_interval: 14400            # Scrape every 4 hours
    value_template: '{{ value_json.FirstHighTide }}'
    json_attributes:
      - PeakTimes
      - PeakHeights
```


