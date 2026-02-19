# World of Transport

Command-line app that lists transport hubs within a given distance

## Requirements

- Python 3.14.3+
- No external dependencies
  
## Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/World_of_Transport.git

cd world-of-transport

## Usage

python app.py <latitude> <longitude> <distance_km>

Example:

python app.py 47.5 19.2 50

## Notes

- Pulls data from https://mikerhodes.cloudant.com/airportdb
- Uses search index _design/view1/_search/geo
- The default limit(25) for the queries not bypassed
- Calculations are rough approximations
- Results are sorted by ascending distance

## Sources
https://www.askpython.com/python/examples/calculate-gps-distance-using-haversine-formula

https://stackoverflow.com/questions/1253499/simple-calculations-for-working-with-lat-lon-and-km-distance
