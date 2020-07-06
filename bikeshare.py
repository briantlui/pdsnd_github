import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input("Would you like to see data from Chicago, New York, or Washington?\n")
        if city.title() not in ('Chicago', 'New York','Washington'):
            print('Your selection is not valid.\n')
            continue
        else:
            print("\nLet's look into data from {}!\n".format(city.title()))
            break
    while True:
        month = input("Which month would you like to filter by? January, February, March, April, May, June, or All (for all months).\n")
        if month.title() not in ('January', 'February', 'March', 'April', 'May', 'June','All'):
            print('Your selection is not valid.\n')
            continue
        elif month.title() in ('January', 'February', 'March', 'April', 'May', 'June'):
            print("\nLet's look into data from {}\n".format(month.title()))
            break
        else:
            print("\nYou have selected to look at All months.\n")
            break

    while True:
        day = input("Which day would you like to filter by? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or All (for all days of the week). \n")
        if day.title() not in ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All'):
            print('Your selection is not valid.\n')
            continue
        elif day.title() in ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'):
            print("\nLet's look into data from {}\n".format(day.title()))
            break
        else:
            print("You have selected to look at All days.")
            break
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month #returns month as an integer
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month.title() != 'All':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day.title() != 'All':
        df = df[df['day_of_week']==day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    pop_month = df['month'].mode()[0]
    pop_month = calendar.month_name[pop_month]
    print("The most popular month is: ",pop_month)

    pop_dow = df['day_of_week'].mode()[0]
    print("The most popular day of the week is: ",pop_dow)

    df['hour'] = df['Start Time'].dt.hour
    pop_start_hour = df['hour'].mode()[0]
    print("The most common start hour is: ",pop_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    pop_start_station = df['Start Station'].mode()[0]
    print("The most popular start station is: ",pop_start_station)

    pop_end_station = df['End Station'].mode()[0]
    print("The most popular end station is: ",pop_end_station)

    df['StartEnd'] = "From " + df['Start Station'] + " To "+ df['End Station']
    pop_route = df.groupby('StartEnd')['StartEnd'].count().idxmax()
    print('The most populart route is: ',pop_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def conv_time(seconds):
    """Converts seconds into Days, Hours, Minutes, and Seconds"""

    time = float(seconds)
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    return("{} days, {} hours, {} minutes, and {} seconds".format(day,hour,minutes,seconds))

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time = df['Trip Duration'].sum()
    total_time = conv_time(total_time)
    print("The total time traveled was: {}".format(total_time))

    average_time = df['Trip Duration'].mean()
    average_time %= 3600
    minutes = average_time // 60
    average_time %= 60
    seconds = average_time
    print("The average time traveled was: {} minutes and {} seconds".format(minutes,seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        u = df['User Type'].value_counts()
        print("User Type Counts:\n",u.to_string())
    except KeyError:
        print("User Type Data Not Available...")

    try:
        g = df['Gender'].value_counts()
        print("\nGender Counts:\n",g.to_string())
    except KeyError:
        print("\nGender Data Not Available...\n")

    try:
        print("\nEarliest birth year: ", int(df['Birth Year'].min()))
        print("Most recent birth year: ", int(df['Birth Year'].max()))
        print("Most common birth year: ", int(df['Birth Year'].value_counts().idxmax()))
    except KeyError:
        print("\nBirth Year Data Not Available...\n")
    finally:
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def raw_input(df):
    """
    Loop to asks user if they would see the next 5 lines of raw data.
    Continues to display data if user inputs 'yes'. Stops when user inputs "no"
    """
    start_time = time.time()
    raw = np.array([0,1,2,3,4])
    while True:
        user_input = input("Would you like to see the raw data? Enter yes or no.\n")
        if user_input.lower() != "yes":
            break
        if user_input.lower() == "yes":
            print(df.iloc[raw])
            raw += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_input(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
