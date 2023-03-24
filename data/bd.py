import sqlite3


class DataBase:
    def __init__(self, bd_file):
        self.connection = sqlite3.connect(bd_file)
        self.cursor = self.connection
        self.connection.execute('CREATE TABLE IF NOT EXISTS stock (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                                'country,'
                                'category,'
                                'id_photo,'
                                'product_name,'
                                'specifications,'
                                'price,'
                                'count,'
                                'number_of_orders INTEGER DEFAULT 0,'
                                'value INTEGER DEFAULT 1)')
        self.connection.execute('CREATE TABLE IF NOT EXISTS countries (country)')
        self.connection.execute('CREATE TABLE IF NOT EXISTS categories (category)')
        self.connection.execute('CREATE TABLE IF NOT EXISTS users (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT '
                                'NULL,'
                                'category,'
                                'user_id,'
                                'user_phone,'
                                'user_name,'
                                'reg_date,'
                                'last_purchase INTEGER DEFAULT 1,'
                                'last_purchase_date INTEGER DEFAULT 1,'
                                'total_money INTEGER DEFAULT 1)')

        self.connection.execute('CREATE TABLE IF NOT EXISTS basket'
                                '(user_id,'
                                'id_product,'
                                'count)')
        self.connection.commit()

    """*********************Проверки существования в базе*******************************"""

    def bd_checks_for_country(self):
        """запрос стран для админа"""
        try:
            with self.connection:
                x = self.cursor.execute("SELECT country FROM countries").fetchall()
                return [i[0] for i in x]
        except IndexError:
            return []

    def bd_checks_for_categories(self):
        """запрос категорий для админа"""
        try:
            with self.connection:
                x = self.cursor.execute("SELECT category FROM categories").fetchall()
                return [i[0] for i in x]
        except IndexError:
            return []

    def bd_checks_for_country_in_stock(self):
        """запрос стран для user"""
        try:
            with self.connection:
                x = self.cursor.execute("SELECT country FROM stock").fetchall()
                return [i[0] for i in x]
        except IndexError:
            return []

    def bd_checks_for_category_in_stock(self, counter):
        """запрос категорий для user"""
        try:
            with self.connection:
                x = self.cursor.execute("SELECT category FROM stock WHERE country = ?",
                                        (counter,)).fetchall()
                return [i[0] for i in x]
        except IndexError:
            return []

    def bd_checks_for_category_product_in_stock(self, counter, category):
        """Отдаёт user список продуктов по стране и категории если продукт в наличии (количество более 1 шт)
        и флаг value = 1"""
        try:
            with self.connection:
                return self.cursor.execute("SELECT * FROM stock WHERE country = ? AND category = ? AND count > 1 ",
                                           (counter, category)).fetchall()
        except IndexError:
            return []

    """*********************************************************************************"""

    """*********************Изменение значений в существующих записях ********************************************"""
    def changes_count_in_basket(self, user_id, id_product):
        """Изменение количества товара в корзине yf +1"""
        with self.connection:
            self.cursor.execute("UPDATE basket SET count = count + 1 WHERE user_id = ? AND id_product = ?",
                                (user_id, id_product))
    """*********************************************************************************"""

    """*********************Добавление в базу*******************************************"""

    def bd_add_country(self, country):
        with self.connection:
            self.cursor.execute("INSERT INTO countries (country) VALUES (?)", (country,))
            self.connection.commit()

    def bd_add_category(self, categories):
        with self.connection:
            for cat_y in categories:
                self.cursor.execute("INSERT INTO categories (category) VALUES (?)", (cat_y,))
            self.connection.commit()

    def bd_add_product_in_stock(self, product):
        with self.connection:
            self.cursor.execute("INSERT INTO stock "
                                "(country, category, id_photo, product_name, specifications, price,count) "
                                "VALUES (?, ?, ?, ?, ?, ?, ?)", product)
            self.connection.commit()

    def bd_add_product_in_basket(self, user_id, id_product, count=1):
        """Запись товара добавленогов корзину но не купленого"""
        with self.connection:
            self.cursor.execute("INSERT INTO basket (user_id, id_product, count) VALUES (?, ?, ?)",
                                (user_id, id_product, count))

    '''*********************************************************************************'''
# db = DataBase('database.db')
# # db.add_product_in_basket(22, 55)
# db.changes_count_in_basket(22, 55)
