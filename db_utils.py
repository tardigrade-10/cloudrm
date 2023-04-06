import mysql.connector

def get_connection():
    mydb = mysql.connector.connect(
        host="mysql",
        user="root",
        password="password"
        )

    # Create a database
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS cloudrm_db")

    # Connect to the database
    mydb = mysql.connector.connect(
        host="mysql",
        user="root",
        password="password",
        database="cloudrm_db"
    )

    # Create the images table
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS images (id INT AUTO_INCREMENT PRIMARY KEY, inp_path VARCHAR(255), pred_path VARCHAR(255))")
    mycursor.close()

    return mydb 

# insert input image path to mysql db
def insert_input(inp_path):

    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO images (inp_path) VALUES (%s)"
    values = (inp_path,)
    cursor.execute(query, values)
    connection.commit()
    print(f"Image {inp_path} inserted successfully.")
    cursor.close()
    connection.close()

# insert predicted image path to mysql db
def insert_pred(inp_path, pred_path):

    connection = get_connection()
    cursor = connection.cursor()
    query = "UPDATE images SET pred_path = %s WHERE inp_path = %s"
    values = (pred_path, inp_path)
    cursor.execute(query, values)
    connection.commit()
    print(f"Pred Path {pred_path} inserted successfully for {inp_path}.")
    cursor.close()
    connection.close()
