import psycopg2
import json
from typing import List, Dict, Optional, Any


class PostgresDB:
    def __init__(self, host, user, password, port):
        self.host = host
        self.user = user
        self.password = password
        self.port = port

    def create_database(self, db_name):

        conn = psycopg2.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name}")
        cursor.close()
        conn.close()
        print(f"Database '{db_name}' created successfully")

    def create_table_vacancies(self, db_name):
        conn = psycopg2.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=db_name
        )
        conn.autocommit = True
        cursor = conn.cursor()
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS vacancies (
                    index SERIAL,
                    id  VARCHAR(255) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    salary_currency VARCHAR(255),
                    url_vacancy VARCHAR(255),
                    employer_id VARCHAR(255),
                    employer_name VARCHAR(255),
                    requirement TEXT,
                    responsibility TEXT)
                    """
            )

        conn.commit()
        conn.close()

    def insert_data_vacancies(self, db_name, data_vacancies):
        conn = psycopg2.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=db_name
        )

        with conn.cursor() as cur:
            for vacancy in data_vacancies:
                cur.execute(
                    """
                    INSERT INTO vacancies (id, name, salary_from, salary_to, salary_currency, url_vacancy, employer_id, 
                    employer_name, requirement, responsibility)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING index
                    """,
                    (
                        vacancy["id"],
                        vacancy["name"],
                        vacancy["salary_from"],
                        vacancy["salary_to"],
                        vacancy["salary_currency"],
                        vacancy["url_vacancy"],
                        vacancy["employer_id"],
                        vacancy["employer_name"],
                        vacancy["requirement"],
                        vacancy["responsibility"],
                    ),
                )
                index = cur.fetchone()[0]

        conn.commit()
        conn.close()

    def create_table_emloyers(self, db_name):
        conn = psycopg2.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=db_name
        )
        conn.autocommit = True
        cursor = conn.cursor()
        with conn.cursor() as cur:
            cur.execute(
                """
                   CREATE TABLE IF NOT EXISTS employers (
                       index SERIAL,
                       id  VARCHAR(255) PRIMARY KEY,
                       name VARCHAR(255) NOT NULL,
                       url_hh_employer VARCHAR(255)
                       )
                       """
            )
        conn.commit()
        conn.close()

    def insert_data_empoloyers(self, db_name, data_emlpoyers):
        conn = psycopg2.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=db_name
        )

        with conn.cursor() as cur:
            for employer in data_emlpoyers:
                cur.execute(
                    """
                    INSERT INTO employers (id, name, url_hh_employer)
                    VALUES (%s, %s, %s)
                    RETURNING index
                    """,
                    (employer["id"], employer["name"], employer["url_hh_employer"]),
                )
                index = cur.fetchone()[0]

        conn.commit()
        conn.close()

    @classmethod
    def created_postgres_conn(cls, data):
        host = data.get("host")
        port = data.get("port")
        user = data.get("user")
        password = data.get("password")

        return cls(host=host, port=port, user=user, password=password)
