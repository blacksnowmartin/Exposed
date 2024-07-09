import sqlite3

# Connect to the database
conn = sqlite3.connect('facebook_database.db')
cursor = conn.cursor()

# Execute SQL query to extract all passwords
cursor.execute("SELECT password FROM users")

# Fetch all the results
passwords = cursor.fetchall()

# Print all the extracted passwords
for password in passwords:
    print(password[0])

# Close the connection
conn.close()
