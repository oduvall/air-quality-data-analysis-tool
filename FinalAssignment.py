""" This program runs an interactive database for analyzing PurpleAir
air quality data.
"""
import csv
from enum import Enum


filename = './purple_air.csv'


class Stats(Enum):
    """ Enums that contain indices of their namesake's calculation.

    Attribute:
        MIN (enum): Index of min in tuple returned from a call to
            _cross_table_statistics.
        AVG (enum): Index of average in tuple returned from a call to
            _cross_table_statistics.
        MAX (enum): Index of max in tuple returned from a call to
            _cross_table_statistics.
    """
    MIN = 0
    AVG = 1
    MAX = 2


class EmptyDatasetError(Exception):
    pass


class NoMatchingItems(Exception):
    pass


class DataSet:
    """ Contains purple air quality data and methods for analysis.

    Attribute:
        _header: A string value containing the header of the data set.
        _data: A list of 3-element tuples containing a string that holds a
            zip code, a string that holds a time of day, and a float value
            for concentration data.
        _zips: A dictionary of unique zip code strings as keys and
            Booleans for values.
        _times: A list of unique time of day strings.
    """
    def __init__(self, header=""):
        """ Initializes DataSet.

        Args:
            header (str): Input for the header of the data set.
                Defaults to the empty string.
        """
        self.header = header
        self._data = None
        self._zips = {}
        self._times = []

    def _cross_table_statistics(self, descriptor_one: str,
                                descriptor_two: str) -> tuple:
        """ Return summary statistics from the filtered data set.

        Args:
            descriptor_one (str): Input for matching zip code.
            descriptor_two (str): Input for matching time of day.

        Returns:
            tuple: Minimum, average, and maximum concentrations from
                the filtered data.
        """
        if not isinstance(self._data, list) or len(self._data) == 0:
            raise EmptyDatasetError
        matched_data = [row[2] for row in self._data
                        if row[0] == descriptor_one
                        and row[1] == descriptor_two]
        if len(matched_data) == 0:
            raise NoMatchingItems
        return (min(matched_data), sum(matched_data)/len(matched_data),
                max(matched_data))

    def load_default_data(self):
        """ Set self._data to default data and initialize labels. """
        self._data = [
            ("12345", "Morning", 1.1),
            ("94022", "Morning", 2.2),
            ("94040", "Morning", 3.0),
            ("94022", "Midday", 1.0),
            ("94040", "Morning", 1.0),
            ("94022", "Evening", 3.2)
        ]
        self._initialize_labels()

    def load_file(self):
        """ Load data from Purple Air data file to self._data. """
        with open(filename, 'r', newline='') as file:
            csvreader = csv.reader(file)
            self._data = [(row[1], row[4], float(row[5])) for row in csvreader
                          if row[1] != 'Approximate Zip Code']
            self._initialize_labels()
        print(f"{len(self._data)} lines loaded.")

    def _initialize_labels(self):
        """ Initialize zip code and time of day labels.

        Map a dictionary of unique zip codes and a list of times from
        self._data to self._zips and self._times.
        """
        zips = {}
        times = set()
        for row in self._data:
            zips[row[0]] = True
            times.add(row[1])
        self._zips = zips
        self._times = list(times)

    def display_cross_table(self, stat: Stats):
        """ Print table of selected air quality statistics.

        Args:
            stat (Stats): One of Stats.MIN, Stats.AVG, or Stats.MAX.
                Selects which summary statistic the table will display.
        """
        if not isinstance(self._data, list) or len(self._data) == 0:
            print("No data is loaded. Please load the data set.")
        else:
            # Print table header:
            print("")
            print(f"{'       ':<}", end="")
            for time_of_day in self._times:
                print(f"{time_of_day:>8}", end="")
            print("")

            # Print table rows:
            for zip_code in self._zips:
                if not self._zips[zip_code]:
                    continue
                else:
                    print(f"{zip_code:<7}", end="")
                    for time_of_day in self._times:
                        try:
                            min_max_avg = self._cross_table_statistics(
                                zip_code, time_of_day)
                        except NoMatchingItems:
                            min_max_avg = "N/A"
                        if min_max_avg == "N/A":
                            print(f"{'N/A':>8}", end="")
                        else:
                            print(f"{min_max_avg[stat.value]:>8.2f}", end="")
                    print("")

    @property
    def header(self) -> str:
        return self._header

    @header.setter
    def header(self, header: str):
        if len(header) <= 30:
            self._header = header
        else:
            raise ValueError

    def get_data(self) -> list:
        """ Return a copy of self._data list."""
        if self._data is None:
            return [None]
        else:
            return self._data.copy()

    def get_zips(self) -> dict:
        """ Return a copy of self._zips dictionary. """
        return self._zips.copy()

    def toggle_zip(self, target_zip: str):
        """ Change Boolean value associated with target_zip.

        Args:
            target_zip (str): Zip code the user wishes to toggle.
        """
        if target_zip not in self._zips:
            raise LookupError
        else:
            self._zips[target_zip] = not self._zips[target_zip]


def main():
    """ Run the program.

    Prompt the user to input their name and then print a greeting
    including their name. Afterwards, prompt the user to input a header
    for the menu, and then call menu().
    """
    user_name = input("Please enter your name: ")
    print(f"Hello {user_name}, welcome to the Air Quality database.")
    purple_air = DataSet()
    while True:
        try:
            purple_air.header = input(
                "Now please enter a header for the menu: "
            )
            break
        except ValueError:
            print("Header must a string that is at most 30 characters long.")
            continue
    print("\n")
    menu(purple_air)


def print_menu():
    """ Print the main menu.

    Print the main menu items alongside their numbers in
    chronological order.
    """
    print("Main Menu")
    print("1 - Print Average Particulate Concentration by Zip Code and Time")
    print("2 - Print Minimum Particulate Concentration by Zip Code and Time")
    print("3 - Print Maximum Particulate Concentration by Zip Code and Time")
    print("4 - Adjust Zip Code Filters")
    print("5 - Load Data")
    print("9 - Quit")


def menu(my_dataset: DataSet):
    """ Handle user menu item selection.

    Args:
        my_dataset (DataSet): Object that contains the air quality data.

    In a while loop, print the DataSet header and menu options, then
    prompt the user to enter a number as an input. Run the function
    that corresponds to the number the user inputs.
    """
    valid_menu_options = {
        1: lambda: my_dataset.display_cross_table(Stats.AVG),
        2: lambda: my_dataset.display_cross_table(Stats.MIN),
        3: lambda: my_dataset.display_cross_table(Stats.MAX),
        4: lambda: manage_filters(my_dataset),
        5: my_dataset.load_file,
    }
    while True:
        print(my_dataset.header)
        print_menu()
        number_selected = input("What is your choice? ")
        try:
            number_as_int = int(number_selected)
        except ValueError:
            print("Please enter a number next time.", "\n")
            continue
        if number_as_int == 9:
            print("Exiting database. Goodbye.", "\n")
            break
        elif number_as_int in valid_menu_options:
            valid_menu_options[number_as_int]()
            print("")
        else:
            print("That is not a valid selection. Please choose "
                  "something else.", "\n")


def manage_filters(my_dataset: DataSet):
    """ Handle user toggling zip code filters.

    Args:
        my_dataset (DataSet): Object that contains the air quality data.
    """
    if (not isinstance(my_dataset.get_data(), list) or
            my_dataset.get_data()[0] is None):
        print("No data is loaded. Please load the data set.")
    else:
        while True:
            print("The following labels are in the data set:")
            gotten_zips = my_dataset.get_zips()
            for i, zips in enumerate(gotten_zips, 1):
                print(f"{i}: {zips:11}"
                      f"""{'ACTIVE' if gotten_zips[zips] == True 
                      else 'INACTIVE':<}""")
            selected_zip = input("Please select an item to toggle or press "
                                 "enter/return when you are finished.")
            if selected_zip == "":
                break
            try:
                selected_zip = int(selected_zip)
            except ValueError:
                print("Please enter a number next time.")
                continue
            found = False
            for i, zips in enumerate(gotten_zips, 1):
                if i == selected_zip:
                    my_dataset.toggle_zip(zips)
                    found = True
                    break
            if not found:
                print("That is not a valid selection. Please choose "
                      "something else.")


if __name__ == "__main__":
    main()

r"""
--- sample run ---
Please enter your name: Owen
Hello Owen, welcome to the Air Quality database.
Now please enter a header for the menu: The Last Header :D


The Last Header :D
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 1
No data is loaded. Please load the data set.

The Last Header :D
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 5
6147 lines loaded.

The Last Header :D
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 1

          Night Morning Evening  Midday
94028      1.58    1.54    2.26    2.92
94304      1.23    1.36    1.17    2.89
94022      1.32    1.50    1.22    2.92
94024      1.69    1.71    3.42    3.27
94040      2.47    1.86    4.57    3.28
94087      2.31    2.24    4.77    3.92
94041      3.43    2.41    4.53    3.52
95014      2.19    1.06    2.38    3.29

The Last Header :D
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 2

          Night Morning Evening  Midday
94028      0.00    0.00    0.00    0.00
94304      0.00    0.00    0.00    0.00
94022      0.00    0.00    0.00    0.00
94024      0.00    0.00    0.00    0.00
94040      0.00    0.00    0.00    0.00
94087      0.00    0.00    0.00    0.00
94041      0.00    0.00    0.00    0.00
95014      0.00    0.00    0.00    0.00

The Last Header :D
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 3

          Night Morning Evening  Midday
94028     25.00   25.72   79.88   24.21
94304      9.92    9.66    9.73   20.93
94022     14.38   12.90   11.53   26.59
94024      9.67   15.12   37.57   29.17
94040     20.34   10.49   44.05   25.95
94087     13.14    9.39   38.11   26.48
94041     19.67    8.02   31.82   25.89
95014     37.82    9.95   69.05   25.00

The Last Header :D
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 4
The following labels are in the data set:
1: 94028      ACTIVE
2: 94304      ACTIVE
3: 94022      ACTIVE
4: 94024      ACTIVE
5: 94040      ACTIVE
6: 94087      ACTIVE
7: 94041      ACTIVE
8: 95014      ACTIVE
Please select an item to toggle or press enter/return when you are finished.8
The following labels are in the data set:
1: 94028      ACTIVE
2: 94304      ACTIVE
3: 94022      ACTIVE
4: 94024      ACTIVE
5: 94040      ACTIVE
6: 94087      ACTIVE
7: 94041      ACTIVE
8: 95014      INACTIVE
Please select an item to toggle or press enter/return when you are finished.

The Last Header :D
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 3

          Night Morning Evening  Midday
94028     25.00   25.72   79.88   24.21
94304      9.92    9.66    9.73   20.93
94022     14.38   12.90   11.53   26.59
94024      9.67   15.12   37.57   29.17
94040     20.34   10.49   44.05   25.95
94087     13.14    9.39   38.11   26.48
94041     19.67    8.02   31.82   25.89

The Last Header :D
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 9
Exiting database. Goodbye. 

"""