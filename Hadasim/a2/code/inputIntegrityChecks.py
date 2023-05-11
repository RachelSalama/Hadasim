from datetime import datetime
from handelDB import get_curser_HMODB


# this function checks if client already exists in clients table
def check_client_exist(id, table):
    mycursor, myconn = get_curser_HMODB()
    mycursor.execute(f"SELECT * FROM {table} WHERE ID = ?", (id,))
    # Check if the SELECT statement returned any rows
    if mycursor.fetchall():
        myconn.close()
        return True
    myconn.close()
    return False


# this function checks the integrity and order of the dates input
def date_is_before(date1, date2):
    if(not date1):
        date1= datetime.now()
    else:
        try:
            date1= datetime.strptime(date1, "%d-%m-%Y")
        except:
            return True #date is wrong format or wrong. format should be as following: dd-mm-yyyy'
    try:
        date2 = datetime.strptime(date2, "%d-%m-%Y")
    except:
        return True #either date format is wrong or date is wrong. format should be as following: dd-mm-yyyy'

    if(date2.date() >= date1.date() or date2.date().year+120 <= datetime.now().year):#if date thats sppouse to be later than other date comes before
        return True
    return False

# this function checks the integrity of the input to clients table
def check_input_integrity_client(id, dateOfBirth, phoneNumber, mobile):
    if(len(id)==9 and id.isdigit()):#if id in correct length and containes only numbers
        if (check_client_exist(id, 'clients')):
            return True, f'client already exists in the table'
    else:
        return True, f'id is not valid'

    if(date_is_before(None, dateOfBirth)):#check if given dateofbirth is in the futre
        return True, f'date of birth is wrong'
    if(len(phoneNumber) != 9 or phoneNumber[0]!='0' and phoneNumber.isdigit()):#if phoneNumber in wrong length or dosnt start with correct digit
        return True, f'invalid phone number'
    if (len(mobile) != 10 or mobile[0]!='0' or mobile[1]!='5' and phoneNumber.isdigit()):
        return True, f'invalid mobile number'
    return False, ""

# this function checks the integrity of the input to covid table
def check_input_integrity_covid(id, vaccinationDate1, vaccinationDate2, \
               vaccinationDate3, vaccinationDate4, positiveResDate, dateOfRecovery):
    if (not check_client_exist(id, 'clients')):
        return True, f'id of client dosnt exist in clients table'
    if(check_client_exist(id, 'covid')):
        return True, f'client already exist in covids table'
    if(vaccinationDate1):# only if client is vaccinated checkintegrity of dates
        if (date_is_before(vaccinationDate2, vaccinationDate1)):#if vaccinationDate2 if before vaccinationDate1
            return True, f'First vaccination Date or Second vaccination Date is wrong'
        if (date_is_before(vaccinationDate3, vaccinationDate2)):#if vaccinationDate3 if before vaccinationDate2
            return True, f'Third vaccination Date or Second vaccination Date is wrong'
        if (date_is_before(vaccinationDate4, vaccinationDate3)):#if vaccinationDate4 if before vaccinationDate3
            return True, f'Fourth vaccination Date or Third vaccination Date is wrong'
        if (date_is_before(dateOfRecovery, positiveResDate)):#if date Of Recovery if before positive Result Date
            return True, f'date Of Recovery or positive Result Date is wrong'
    return False, ""