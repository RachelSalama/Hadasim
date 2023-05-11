import datetime
import sqlite3


# this function returns a curser and conn to HMO data base
def get_curser_HMODB():
    conn = sqlite3.connect(r"HMO.db")
    mycursor = conn.cursor()
    return (mycursor, conn)


# this function creates a clients table in HMO.db
def create_clients_table():
    mycursor, myconn = get_curser_HMODB()
    myconn.text_factory = bytes
    try:
        myconn.executescript(""" CREATE TABLE IF NOT EXISTS clients (
                                                    Name VARCHAR(255) NOT NULL,
                                                    LastName VARCHAR(255) NOT NULL,
                                                    ID TEXT PRIMARY KEY,
                                                    City VARCHAR(255) NOT NULL,
                                                    Street VARCHAR(255) NOT NULL,
                                                    HouseNum VARCHAR(255) NOT NULL,
                                                    DateOfBirth TEXT NOT NULL,
                                                    PhoneNumber VARCHAR(9) NOT NULL,
                                                    Mobile VARCHAR(10),
                                                    Img BLOB
                                                ); """)
        myconn.commit()
        myconn.close()
    except:
        print("unable to create clients table")
        myconn.close()


# this function creates a clients covid details table in HMO.db
def create_covid_table():
    mycursor, myconn = get_curser_HMODB()
    myconn.text_factory = bytes
    try:
        myconn.executescript(""" CREATE TABLE IF NOT EXISTS covid (
                                                       ID TEXT PRIMARY KEY,
                                                       VaccinationDate1 TEXT,
                                                       VaccineManufacturer1 VARCHAR(255),
                                                       VaccinationDate2 TEXT,
                                                       VaccineManufacturer2 VARCHAR(255),
                                                       VaccinationDate3 TEXT,
                                                       VaccineManufacturer3 VARCHAR(255),
                                                       VaccinationDate4 TEXT,
                                                       VaccineManufacturer4 VARCHAR(255),
                                                       PositiveResDate TEXT NOT NULL,
                                                       DateOfRecovery TEXT
                                                   ); """)

        myconn.commit()
        myconn.close()
    except:
        print("Table was not created, Possibly already exists")
        myconn.close()


# this function returns amount of patients with covid in last month per day
def get_active_corona_patients():
    mycursor, myconn = get_curser_HMODB()
    month = datetime.datetime.now().month-1
    year = datetime.datetime.now().year
    if(month==0):# if current month is jan update year and month for last month
        month=12
        year -=1
    mycursor.execute("SELECT PositiveResDate FROM covid")
    rows = mycursor.fetchall()
    # Create two empty lists for dates and counts
    dates = []
    counts = []

    # Iterate through all rows and count patients with PositiveResDate in last month
    for row in rows:
        date_str = row[0]  # Get the date string from the row
        date_obj = datetime.datetime.strptime(date_str, '%d-%m-%Y')
        if date_obj.strftime('%Y-%m') == f"{year}-{month:02}":  # Check if date is in last month
            if date_obj.date() not in dates:  # If date not already in dates list, add it and set count to 1
                dates.append(date_obj.date())
                counts.append(1)
            else:  # If date already in dates list, increment count
                index = dates.index(date_obj.date())
                counts[index] += 1

    ret = f"{sum(counts)} clients were ill this month. "
    return counts, dates

