[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue)](https://docs.python.org/release/3.9.23/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue)](https://docs.python.org/release/3.11.12/)

# Create the venv (tested with 3.9 and 3.11 also works on raspbian/arm)

```
python3.9 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

# create the credentials file
```
python create_token.py
```

# Test the job (expects camera named "Front Garden"), schedule this in cron.

Will output .log and .jpg in current working directory. 

```
python run_blink.py
```

# Suggested cron frequencies for time lapse (During Daylight Only):

1. Every 6 hours (2xday) : 8 AM and 2 PM
   Good for slow changes

2. Every 4 hours (3xday) : 8 AM, 12 PM, 4 PM
   More natural flow, captures morning/midday/evening light

3. Every 2 hours (7x/day) : 6 AM, 8 AM, 10 AM, 12 PM, 2 PM, 4 PM, 6 PM
   Very smooth, excellent for fast plant movements like flowers opening

```
0 8,12,16 * * * cd /opt/blink_time_lapse && /opt/blink_time_lapse/.env/bin/python3 run_blink.py
```

# filtering the log

JSON
```
jq '{iso_time,temperature_c,battery_voltage}' front_garden.log
```

CSV
```
jq -r '[.iso_time, .temperature_c, .battery_voltage] | @csv' front_garden.log
```
