### ETL Project - NHL Salary cap
The project is to collect data on NHL teams salary caps, the most contributing players, and scrape the franchise logo

## Project
1. Data World contains a list of NHL player salaries .  Using Python via Jupyter notebook, I collected the file from the webiste and cleaned it for compatibility with other data sites (specifically, renamed colums(s) and corrected a team abbreviation).

2. NHL.com contains a statistics API for teams and players.  A little searching yielded a JSON file with the 31 active NHL teams and their related details

3. From the above data sources I was able to clean the data to construct DataFrames of
    a. Each team's salary cap
    b. A list of the most contributing player to the salary cap
    c. Extract the necessary fields to scrape the team's logo from its NHL site
   employing various techniques to complete the transformations needed.

4. I constructed lists necessary for insert to the local mongo database
    a. Team name 
    b. Salary cap 
    c. Player
    d. Player's salary
    e. URL to each team's official logo from NHL website (This was challenging!)

5. The data from step 4 was pushed to a local mondgoDB for accessibility and portability.


## Out of scope
I had developed an HTML page to display this ETL data including logos but ran out of time due to uncommon HTML issues which, with additional time, I will sort and can display this data.