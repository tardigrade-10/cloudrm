import mysql.connector

# DATABASE_URI = "mysql"

def get_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password"
        )

    # Create a database
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS cloudrm_db")

    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="cloudrm_db"
    )

    # Create the images table
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS images (id INT AUTO_INCREMENT PRIMARY KEY, inp_path VARCHAR(255), pred_path VARCHAR(255))")
    # mycursor.execute("CREATE TABLE IF NOT EXISTS predictions (id INT AUTO_INCREMENT PRIMARY KEY, image_id INT, predicted_image_path VARCHAR(255))")
    mycursor.close()

    return mydb 

def insert_input(inp_path):
    # try:
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO images (inp_path) VALUES (%s)"
    values = (inp_path,)
    cursor.execute(query, values)
    connection.commit()
    print(f"Image {inp_path} inserted successfully.")
# except Exception as e:
    # print(f"Error inserting image {inp_path}: {e}")
# finally:
    cursor.close()
    connection.close()

def insert_pred(inp_path, pred_path):
# try:
    connection = get_connection()
    cursor = connection.cursor()
    query = "UPDATE images SET pred_path = %s WHERE inp_path = %s"
    values = (pred_path, inp_path)
    cursor.execute(query, values)
    connection.commit()
    print(f"Pred Path {pred_path} inserted successfully for {inp_path}.")
# except Exception as e:
    # print(f"Error inserting pred path {pred_path}: {e}")
# finally:
    cursor.close()
    connection.close()
