import datetime
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import sqlite3
from io import BytesIO
from flask import Response
from flask import Flask, request, send_file
from matplotlib.ticker import MaxNLocator
from handelDB import create_clients_table, get_curser_HMODB, create_covid_table, \
    get_active_corona_patients
from inputIntegrityChecks import check_input_integrity_client,check_client_exist, check_input_integrity_covid

app = Flask(__name__)


create_clients_table()
create_covid_table()

# This function gets cliet details and adds a record to clients table
@app.route('/api/add_client/<name>/<lastName>/<id>/<city>/<street>/<houseNum>/<dateOfBirth>/<phoneNumber>/<mobile>')
def add_client(name, lastName, id, city, street, houseNum, dateOfBirth,phoneNumber, mobile):

    error, returnStatment= check_input_integrity_client(id, dateOfBirth,phoneNumber, mobile)
    if error:
        return returnStatment

    mycursor, myconn = get_curser_HMODB()
    sql = 'INSERT INTO clients (Name, LastName, ID, City, Street, HouseNum, DateOfBirth, PhoneNumber, Mobile) VALUES' \
          ' (?, ?, ?, ?, ?, ?, ?, ?, ?)'
    val = [name, lastName,id, city, street, houseNum, dateOfBirth,phoneNumber, mobile]
    try:
        mycursor.execute(sql, val)  # entring clients data to table
        myconn.commit()
        result = f'successfully entered clients details to clients table, <br>'\
                 f'Name: {name}, last name: {lastName}, ID: {id},<br>'\
                 f'city: {city}, street: {street}, house number: {houseNum}<br>'\
                 f'date of birth: {dateOfBirth}, phone number: {phoneNumber}, mobile: {mobile}'

    except Exception as e:
        result = f'failed to enter clients details to clients table: {str(e)}'
    finally:
        myconn.close()
    return result


# This function adds client's covid details to covid table
@app.route('/api/add_client_covid/<id>/<vaccinationDate1>/<vaccineManufacturer1>/<vaccinationDate2>/<vaccineManufacturer2>\
/<vaccinationDate3>/<vaccineManufacturer3>/<vaccinationDate4>/<vaccineManufacturer4>/<positiveResDate>/<dateOfRecovery>')
def add_client_covid(id, vaccinationDate1, vaccineManufacturer1, vaccinationDate2, vaccineManufacturer2,\
               vaccinationDate3, vaccineManufacturer3,vaccinationDate4, vaccineManufacturer4,positiveResDate, dateOfRecovery):

    if vaccinationDate1 == "None":#check if client never vaccinated
        vaccinationDate1 = None

    error, returnStatment = check_input_integrity_covid(id, vaccinationDate1, vaccinationDate2,\
               vaccinationDate3, vaccinationDate4, positiveResDate, dateOfRecovery)
    if error:
        return returnStatment
    mycursor, myconn = get_curser_HMODB()
    sql = 'INSERT INTO covid (ID, VaccinationDate1, VaccineManufacturer1, VaccinationDate2, VaccineManufacturer2,\
            VaccinationDate3, VaccineManufacturer3, VaccinationDate4, VaccineManufacturer4, PositiveResDate, DateOfRecovery)\
            VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    val = [id, vaccinationDate1, vaccineManufacturer1, vaccinationDate2, vaccineManufacturer2, vaccinationDate3,\
           vaccineManufacturer3,vaccinationDate4, vaccineManufacturer4,positiveResDate, dateOfRecovery]
    try:
        mycursor.execute(sql, val)  # entering covid data to table
        myconn.commit()
        result = f'successfully entered clients covid details to covid table, <br>' \
                 f'ID: {id} <br>First vaccination date and manufacturer: {vaccinationDate1}, {vaccineManufacturer1} <br>' \
                 f'Second vaccination date and manufacturer: {vaccinationDate2}, {vaccineManufacturer2} <br>' \
                 f'Third vaccination date and manufacturer: {vaccinationDate3}, {vaccineManufacturer3} <br>' \
                 f'Fourth vaccination date and manufacturer: {vaccinationDate4}, {vaccineManufacturer4} <br>' \
                 f'Positive result date: {positiveResDate} <br> Date of recovery: {dateOfRecovery}'


    except:
        result= f'failed to enter clients covid details to covid table'
    finally:
        myconn.close()
    return result


# This function returns clients details from clients table
@app.route('/api/get_record_client/<id>')
def get_record_client(id):
    if (not check_client_exist(id, 'clients')):
        return "id of client doesn't exist in clients table"
    mycursor, myconn = get_curser_HMODB()
    ClientDetails =[]
    try:
        mycursor.execute("SELECT Name, LastName, ID, City, Street, HouseNum, DateOfBirth, PhoneNumber, Mobile\
         FROM clients WHERE ID = ?", (id,))
        ClientDetails.append(mycursor.fetchall())
    except:
        return f'Error in getting record, check that id is correct: {id}'
    finally:
        myconn.close()
    return ClientDetails[0]


# This function returns covid details for client from covid table
@app.route('/api/get_record_covid/<id>')
def get_record_covid(id):
    if (not check_client_exist(id, 'covid')):
        return f'id of client dosnt exist in covid table'
    mycursor, myconn = get_curser_HMODB()
    arrCovidDetails=[]
    try:
            mycursor.execute("SELECT * FROM covid WHERE ID = ?", (id,))
            arrCovidDetails.append(mycursor.fetchall())
    except:
        return f'Error in getting covid record, check that id is correct: {id}'
    finally:
        myconn.close()
    return arrCovidDetails[0]


#################################################
#Bonus questions


# This function gets id of client and adds image to client's record
@app.route('/api/add_image/<id>', methods=['POST'])
def add_image(id):
    mycursor, myconn = get_curser_HMODB()
    try:
       # check if the ID exists
       mycursor.execute("SELECT ID FROM clients WHERE ID=?", (id,))
       existing_id = mycursor.fetchone()

       if existing_id is None:# ID does not exist in the database
            result = f"Error: ID {id} does not exist in the database"
       else:# ID exists in the database, update the record with the image
            img_data = request.files['image'].read()
            mycursor.execute('UPDATE clients SET Img=? WHERE ID=?', (sqlite3.Binary(img_data), id))
            myconn.commit()
            result = f"Image added to the database with ID: {id}"
    except Exception as e:
        result = f"Failed to add image to the database: {str(e)}"
    finally:
        myconn.close()

    return result


# This function gets id of client and returns image from data base
@app.route('/api/get_image/<id>')
def get_image(id):
    mycursor, myconn = get_curser_HMODB()

    # Retrieve the image data from the database
    try:
        mycursor.execute("SELECT Img FROM clients WHERE id=?", (id,))
        img = mycursor.fetchall()
        img_data = img[0][0]  # Extract image data from the first tuple
        if img_data is None:
            # image does not exist in the database
            return f"Error: Image was not insert in the database for client with id: {id}"
    except Exception as e:
        result = f"Failed to retrieve image from the database: check id correct"
        myconn.close()
        return result
    myconn.close()

    # Return the image as a response to the request
    return send_file(io.BytesIO(img_data), mimetype='image/jpeg')


# This function counts amount of Not Vaccinated clients
@app.route('/api/count_not_vaccinated')
def count_not_vaccinated():
    mycursor, myconn = get_curser_HMODB()

    mycursor.execute("SELECT COUNT(*) FROM clients")
    amountClients = mycursor.fetchall()

    mycursor.execute("SELECT COUNT(*) FROM covid")
    amountVaccinatedClients = mycursor.fetchall()

    mycursor.execute("SELECT COUNT(*) FROM covid WHERE VaccinationDate1 IS NULL")
    amountNotVacciClients = mycursor.fetchall()

    NotVaccinated = (amountClients[0][0] - amountVaccinatedClients[0][0]) + amountNotVacciClients[0][0]
    mycursor.close()
    myconn.close()
    return f"There are {NotVaccinated} clients that are not vaccinated"


# This function counts amount of active corona patients in the last month per day and presents a graph with results
@app.route('/api/active_corona_patients_graph')
def active_corona_patients_graph():
    activeCases, dates = get_active_corona_patients()
    current_date = datetime.datetime.now()
    previous_month = current_date - datetime.timedelta(days=30)
    month = datetime.datetime.strftime(previous_month, "%B %Y")
    fig = Figure()
    FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.bar(dates, activeCases)
    ax.set_title("Active Corona Patients in {}".format(month))
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Active Cases")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    output = BytesIO()
    fig.savefig(output, format='png')
    output.seek(0)

    return Response(output.getvalue(), mimetype='image/png')




if __name__ == '__main__':
    app.run()
