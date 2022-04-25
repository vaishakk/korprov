# Bot for Trafikverket time booking site.
## Usage: 
```
python run.py [-h] [--pn PN] [--test TEST] [--car CAR] [--loc LOC]
              [--add_config]
```
### Arguments:
```
  -h, --help            show this help message and exit 
  --pn PN, -p PN        The personnummer of the user. Format YYYYMMDD-XXXX 
  --test TEST, -t TEST  Test type - Korprov or Kunskapsprov. Default: Korprov 
  --car CAR, -c CAR     Car type - Automatbil or Manuellbil. Default: Automatbil 
  --loc LOC, -l LOC     Location of test. Will be ignored if not a valid location. Default: Farsta
  --add_config 
  ```
### Runing with default values
```
python run.py -p <personnummer>
```
## Configuration
A permenant configuration can be added by calling the --add_config command
```
python run.py --add_config -p <personnummer> -t Kunskapsprov -l Farsta
```
Command line arguments overrides stored configuration.
