# csgo_glicko2

This repository includes code to rank CS:GO pro teams with [Mark Glickman's Glicko-2 Algorithm](http://www.glicko.net/glicko.html) with an own `R` implementation. Data on team's reults comes from [HLTV.org](http://www.hltv.org/?pageid=188&statsfilter=0&offset=0) and is scraped using a `python` script.

## Running the Analysis

* `scraper.py` conatins code for scraping the data from [HLTV.org](http://www.hltv.org/). There are also some Tests at the end.
* `glicko2.R` contains code for calculation rating updates (it follows closely Mark Glickman's suggested implementation which can be found [here](http://www.glicko.net/glicko/glicko2.pdf)).
* `analyze.R` loads the data generated by `scraper.py` and runs the subsequent updates for Glicko-2 ratings.

please run the code in this order to reproduce my results. Scraping the data for 8800 palyed maps will take approximately 2 minutes. All the functions in `glicko2.R` are vectorized and therefore fast for one player vs. an arbitraty number of opponents. The code in `analyze.R` loops over all teams for which to updated the rating in every period which is not properly vectorized, but it will compute in approx. 3 minutes for 23 rating periods and 775 teams, which is fast enough at the moment.

The code is subject to further cleaning and improvements in documentation, but the provided information should be sufficient for anyone who is interested. Please not the License.
