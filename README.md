# interactive-air-quality-analyzer
A simple Python project submission for Foothill College's CS3A class.

## Table of Contents
* [About](#about)
* [Instructions](#instructions)
* [Technologies](#technologies)
* [Setup](#setup)
* [Screenshots](#screenshots)

## About
This is a simple command line data anlysis tool devloped as my final project subission for Foothill College's CS3A "Object-Oriented Programming Methodologies in Python". The user is presented with an interactive menu for analyzing air quality data from PurpleAir based on time of day and zip code. 

## Instructions
1. The user will be prompted to enter their name.
2. The user will be prompted to enter a name for the header of the options menu.
3. Six options will then be presented in the menu: 

    * Print Average Particulate Concentration by Zip Code and Time
    * Print Minimum Particulate Concentration by Zip Code and Time
    * Print Maximum Particulate Concentration by Zip Code and Time
    * Adjust Zip Code Filters
    * Load Data
    * Quit
 
 4. The 'Load Data' option must be chosen before the other commands besides 'Quit' can be run. This option reads and loads the data from the purple_air.csv file.
 5. The top three 'Print' commands each print out a table containing an average, minimum, and maximum measurement, respectively, of air particle concentrations (measured in PPM) based on zip code and time of day (morning, midday, evening, night).
 6. The 'Adjust Zip Code Filters' command allows the user to toggle specific zip codes to be displayed in the tables when printed.
 7. The 'Quit' command terminates the program.
 
 ## Technologies
 * Python 3.10
 
 ## Setup
 1. Clone this repository to your local machine.
 2. From the project root air-quality-data-analysis-tool/, run
 ```
 python3 FinalAssignment.py
 ```
 3. That's it!
 
 ## Screenshots
 <img width="1351" alt="Screen Shot 2022-09-14 at 5 41 40 PM" src="https://user-images.githubusercontent.com/42651770/190287166-719cd4cf-cacd-4002-a8a1-d827d67794fd.png">
<img width="1051" alt="Screen Shot 2022-09-14 at 5 43 17 PM" src="https://user-images.githubusercontent.com/42651770/190287291-aef3b40f-ecda-41d7-9715-3ccb514beb12.png">
