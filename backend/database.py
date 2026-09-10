import sqlite3


DATABASE_NAME = "real_estate_leads.db"


def create_database():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            requirement TEXT,
            location TEXT,
            property_type TEXT,
            configuration TEXT,
            budget TEXT,
            purpose TEXT,
            timeline TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_lead(
    name,
    phone,
    requirement,
    location,
    property_type,
    configuration,
    budget,
    purpose,
    timeline
):
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO leads (
            name,
            phone,
            requirement,
            location,
            property_type,
            configuration,
            budget,
            purpose,
            timeline
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        phone,
        requirement,
        location,
        property_type,
        configuration,
        budget,
        purpose,
        timeline
    ))

    connection.commit()
    connection.close()


def get_all_leads():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM leads")

    leads = cursor.fetchall()

    connection.close()

    return leads