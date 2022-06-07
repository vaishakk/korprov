# Bot for Trafikverket time booking site.
Getting a Swedish driving license is hard enough, but the hardest part is trying to find a time for Kunskapsprov and Körprov. The Trafikverket booking site lists time slots available at each location. It is not possible to list available slots at different locations at once, requiring one to go through each location one after the other in order to find a suitable time slot. This bot automatically crawls through all the prefered test locations and lists the earliest available time-slot at each location, making the process of booking time a little easier for the user. This bot doesn't automatically books a time-slot, but only lists earlier available time-slots at given locations.
## Prerequisites
1. Python 3. Installation [guide](https://docs.python-guide.org/starting/installation/).
2. Latest version of Google Chrome. Download [here](https://www.google.com/intl/en_us/chrome/).
3. Corresponding version of Chrome Driver. Download from [here](https://chromedriver.chromium.org/downloads). Make sure the Chrome driver version matches the version of Google Chrome installed in your computer.

## Installation
1. CD to the location where you want to install.
2. Download the repo to the local drive
```
git clone https://github.com/vaishakk/korprov
```
3. Install dependencies
```
pip3 install -r requirements.txt
```
4. Run the script
```
python run.py -p <personnummer>
``` 
## Usage: 
```
python run.py [-h] [--pn PN] [--test TEST] [--car CAR] [--loc LOC]
              [--add_config]
```
### Arguments:
```
  -h, --help            show this help message and exit
  --pn PN, -p PN        The personnummer of the user.
  --test TEST, -t TEST  Test type - Korprov or Kunskapsprov. Default: Korprov
  --car CAR, -c CAR     Car type - Automatbil or Manuellbil. Default: Automatbil. 
                        Only valid for Korprov.
  --loc LOC, -l LOC     Location of test. 
                        Will be ignored if not a valid location.
  --lang LANG, -s LANG  Language of test. Default: Engelska. 
                        Only valid for Kunskapsprov.
  --add_config
  ```
  [Valid Korprov locations](https://github.com/vaishakk/korprov/blob/main/korprov-locs.txt) \
  [Valid Kunskapsprov locations](https://github.com/vaishakk/korprov/blob/main/kunskaps-locs.txt)

## Configuration
A permenant configuration can be added by calling the --add_config command
```
python run.py --add_config -p <personnummer> -t Kunskapsprov -l Farsta -s Svenska
```
To add many locations to the configuration, run the following command mutiple times until you add all the required locations.
```
python run.py --add_config -l <location>
```
Once all the required locations are added to config, you can run
```
python run.py
```
to scan through all those locations.

Note: Command line arguments overrides stored configuration.
