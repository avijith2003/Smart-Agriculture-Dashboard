import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="popcorns",
        database="weatherapp"
    )

def insert_data(user_id, temperature, humidity, moisture):
    db = connect_to_database()
    cursor = db.cursor()

    sql = "INSERT INTO weather_data (user_id, temperature, humidity, moisture) VALUES (%s, %s, %s, %s)"
    values = (user_id, temperature, humidity, moisture)

    try:
        cursor.execute(sql, values)
        db.commit()
        print("Data inserted successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    # Taking user inputs
    user_id = int(input("Enter User ID: "))
    temperature = float(input("Enter Temperature (e.g. 25.5): "))
    humidity = float(input("Enter Humidity (e.g. 65.00): "))
    moisture = float(input("Enter Soil Moisture (e.g. 23.45): "))

    insert_data(user_id, temperature, humidity, moisture)
