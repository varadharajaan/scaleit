import sqlite3
import logging

from autoscaler_service import log

# Connect to database
conn = sqlite3.connect('instance/your_database_file.db')
c = conn.cursor()

logging.debug("Opened database successfully: ")

# Show tables and columns
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
log.debug(c.fetchall())

# Clear user table
#c.execute("DELETE FROM user;")
#conn.commit()

# Add data in user table only if the user does not exist
selected_user = 'admin'
c.execute("SELECT COUNT(*) FROM user WHERE username=?", (selected_user,))
user_exists = c.fetchone()[0]

if not user_exists:
    c.execute("INSERT INTO user (username, password) VALUES (?, ?);", ('admin', 'admin'))
    conn.commit()
    log.debug("Record created successfully")
else:
    log.debug("User already exists. No record created.")
# Close the database connection
conn.close()