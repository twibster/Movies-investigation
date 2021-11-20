import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'newyork': 'new_york_city.csv',
             'washington': 'washington.csv'}

valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
city_names = ['chicago', 'newyork', 'washington']

def get_filters():
    """
    Gets required filters from the user

    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = input("Enter the name of the city: ").replace(" ","").lower()
    while city not in city_names:   # assures the validity of the input
        city = input("Please enter a valid name: ")

    month = input("Enter the name of the specific month or 'all' for all months:").lower()
    while month not in valid_months:    # assures the validity of the input
        month = input("Please enter a valid name: ")

    day = input("Enter the name of the day or 'all' for all days: ").lower()
    while day not in valid_days:    # assures the validity of the input
        day = input("Please enter a valid name: ")

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        data - Pandas DataFrame containing city data filtered by month and day
    """
    data = pd.read_csv(CITY_DATA[city])
    data['Start Time'] = pd.to_datetime(data["Start Time"])
    data['month'] = data['Start Time'].dt.month
    data['day_of_week'] = data['Start Time'].dt.day_name()
    data['hour']  = data['Start Time'].dt.hour

    if month != 'all':
        month = valid_months.index(month) + 1

        data = data[data['month'] == month]

    if day != 'all':
        data = data[data['day_of_week'] == day.title()]

    return data


def time_stats(data):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    com_month = data["month"].value_counts().keys()[0]
    print('Most common month: {}'.format(valid_months[com_month -1]))

    com_day = data["day_of_week"].value_counts().keys()[0]
    print('Most common day: {}'.format(com_day))

    com_hour = data['hour'].value_counts().keys()[0]
    print("Most common hour of use: {}".format(com_hour))

    print('-' * 40)


def station_stats(data):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')

    com_start_station = data['Start Station'].value_counts().keys()[0]
    print('Most common Start Station: {}'.format(com_start_station))

    com_end_station = data["End Station"].value_counts().keys()[0]
    print('Most common End Station: {}'.format(com_end_station))

    most_frequent_combination = data.groupby(["Start Station"])["End Station"].value_counts().keys()[0]
    print('Most frequent combination of start station and end station: {}'.format(most_frequent_combination))

    print('-' * 40)


def trip_duration_stats(data):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    total_time = (data["Trip Duration"].sum())/ 60
    print('Total travel time in minutes: {}'.format(total_time))

    mean_time = (data["Trip Duration"].mean() /60)
    print('Average travel time in minutes: {}'.format(mean_time))

    print('-' * 40)


def user_stats(data):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')

    user_types = data["User Type"].value_counts()
    print('Counts of user types:\n{}\n'.format(user_types))

    if "Gender" in data.columns:
        gender = data["Gender"].value_counts()
        print('Counts of Gender:\n{}\n'.format(gender))

    if 'Birth Year' in data.columns:
        earliest = data["Birth Year"].min()
        print('Oldest user: {}\n'.format(earliest))

        most_recent = data["Birth Year"].max()
        print('Youngest user: {}\n'.format(most_recent))

        com_year = data["Birth Year"].mode()[0]
        print('Birth year of most users: {}\n'.format(com_year))

    print('-' * 40)


first_time = True

def wanted_stats():
    global first_time
    ''' asks the user to enter the character associated with the information he wants'''

    if first_time == True:
        desired_list = ['R','S']
        wanted_stats.desired = input('Do you want to have a glance at the raw data or detailed statistics?\n(R) for Raw Data\n(S) for Detailed statistics\n').upper()
        first_time = False
        detailed = True
    else:
        desired_list = ['A','B','C','D','X','Y','R','S']
        wanted_stats.desired = input('What information do you want to get insights about ?\n(A) for time_stats \n(B) for station_stats \n(C) for trip_duration_stats \n(D) for user_stats\n(X) to restart\n(Y) to exit\n').upper()
        detailed = False
    while wanted_stats.desired not in desired_list: # assures the validity of the input
        print('Please enter a valid choice')
        if detailed == True:
            wanted_stats.desired = input('Do you want to have a glance at the raw data or detailed statistics?\n(R) for Raw Data\n(S) for Detailed statistics\n').upper()
        else:
            wanted_stats.desired = input('What information do you want to get insights about ?\n(A) for time_stats \n(B) for station_stats \n(C) for trip_duration_stats \n(D) for user_stats\n(X) to restart\n(Y) to exit\n').upper()



def main():
    global first_time
    city, month, day = get_filters()
    while True:
        data = load_data(city, month, day)
        wanted_stats()
        i = 0
        more = 'Y'
        while wanted_stats.desired == 'R' and more == 'Y':
            first_time = False
            raw = data.iloc[i:i+5]
            print(raw)
            i+= 5
            more = input('Do you want to see more? Y for yes - X to exit the raw data section\n').upper()
            choice =['Y','X']
            while more not in choice:
                print('please, choose either Y or X')
                more = input('Do you want to see more? Y for yes - X to exit the raw data section\n').upper()

        if wanted_stats.desired == 'A':
            time_stats(data)
        elif wanted_stats.desired =='B':
            station_stats(data)
        elif wanted_stats.desired =='C':
            trip_duration_stats(data)
        elif wanted_stats.desired =='D':
            user_stats(data)
        elif wanted_stats.desired == 'X':
            first_time = True
            main()
            break
        elif wanted_stats.desired == 'Y':
            break

main()
