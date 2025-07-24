import psycopg2


class DBManager:
    def __init__(self, host, user, password, port, name_base, table_one="employers", table_two="vacancies"):
        self.conn = psycopg2.connect(host=host, port=port, user=user, password=password, database=name_base)
        self.cur = self.conn.cursor()
        self.conn.autocommit = True
        self.table_one = table_one
        self.table_two = table_two

        # def get_data(self, count: int, sort_by: str = 'name') -> list[dict]:
        #     with self.conn:
        #         if sort_by == 'name' or sort_by == 'language':
        #             self.cur.execute(f"SELECT * FROM {self.table_name} ORDER BY {sort_by} ASC LIMIT {count}")
        #         elif sort_by == 'stars' or sort_by == 'forks':
        #             self.cur.execute(f"SELECT * FROM {self.table_name} ORDER BY {sort_by} DESC LIMIT {count}")
        #         else:
        #             self.cur.execute(f"SELECT * FROM {self.table_name} ORDER BY name ASC LIMIT {count}")
        #         data = self.cur.fetchall()
        #         data_dict = [{"name": d[1], "stars": d[2], "forks": d[3], "language": d[4]} for d in data]
        #         return data_dict

    def get_companies_and_vacancies_count(self):
        """ "получает список всех компаний и количество вакансий у каждой компании. В методе используется SQL-запрос,
        выводящий информацию о вакансиях и компаниях через JOIN"""
        with self.conn:
            query = (
                f"SELECT {self.table_one}.name, COUNT({self.table_two}.id) as vacancy_count "
                f"FROM {self.table_one} "
                f"LEFT JOIN {self.table_two} ON {self.table_one}.id = {self.table_two}.employer_id "
                f"GROUP BY {self.table_one}.id "
                f"ORDER BY vacancy_count DESC "
            )

            self.cur.execute(query)
            data = self.cur.fetchall()
            return [{"employer": row[0], "vacancy_count": row[1]} for row in data]

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        В методе используется SQL-запрос, выводящий информацию о вакансиях и компаниях через JOIN."""
        with self.conn:
            query = (
                f"SELECT {self.table_two}.name, {self.table_one}.name, {self.table_two}.salary_from, {self.table_two}.url_vacancy "
                f"FROM {self.table_two} "
                f"LEFT JOIN {self.table_one} ON {self.table_two}.employer_id = {self.table_one}.id "
                f"ORDER BY salary_from DESC "
            )

            self.cur.execute(query)
            data = self.cur.fetchall()
            return [
                {"vacancy": row[0], "employer": row[1], "salary from": row[2], "url_vacancy": row[3]} for row in data
            ]

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям. В методе используется SQL-запрос, выводящий информацию о средней
        зарплате через функцию AVG."""
        with self.conn:
            query = f"SELECT AVG({self.table_two}.salary_from) " f"FROM {self.table_two} "

            self.cur.execute(query)
            data = self.cur.fetchall()
            return [{"avg_salary": float(data[0][0])}]

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        В методе используется SQL-запрос, выводящий информацию о средней зарплате через фильтрацию WHERE."""
        with self.conn:
            query = (
                f"SELECT {self.table_two}.id, {self.table_two}.name, {self.table_two}.salary_from, "
                f"{self.table_two}.salary_to, {self.table_two}.url_vacancy, {self.table_two}.employer_name "
                f"FROM {self.table_two} "
                f"WHERE {self.table_two}.salary_from > (SELECT AVG ({self.table_two}.salary_from) FROM {self.table_two}) "
                f"ORDER BY salary_from "
            )

            self.cur.execute(query)
            data = self.cur.fetchall()
            return [
                {
                    "id": row[0],
                    "vacancy": row[1],
                    "salary from": row[2],
                    "salary_to": row[3],
                    "url_vacancy": row[4],
                    "employer_name": row[5],
                }
                for row in data
            ]

    def get_vacancies_with_keyword(self, word_for_search):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        В методе используется SQL-запрос, выводящий список всех вакансий, в названии которых содержатся переданные
        в метод слова через оператор LIKE."""
        with self.conn:
            like_conditions = " OR ".join([f"name LIKE '%{word}%'" for word in word_for_search])
            query = (
                f"SELECT {self.table_two}.id, {self.table_two}.name, {self.table_two}.url_vacancy, "
                f"{self.table_two}.salary_from "
                f"FROM {self.table_two} WHERE {like_conditions} "
            )
            self.cur.execute(query)
            data = self.cur.fetchall()
            return [{"id": row[0], "vacancy": row[1], "url_vacancy": row[2], "salary_from": row[3]} for row in data]
