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
        self.connection.execute('CREATE TABLE IF NOT EXISTS users (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                                'user_id UNIQUE,'
                                'user_phone INTEGER DEFAULT 1,'
                                'user_name,'
                                'reg_date,'
                                'last_purchase INTEGER DEFAULT 1,'
                                'last_purchase_date INTEGER DEFAULT 1,'
                                'total_money INTEGER DEFAULT 1,'
                                'user_activity INTEGER DEFAULT 1)')

        self.connection.execute('CREATE TABLE IF NOT EXISTS basket'
                                '(user_id,'
                                'id_product,'
                                'count, count_stock, verified INTEGER DEFAULT 0)')

        self.connection.execute('CREATE TABLE IF NOT EXISTS orders '
                                '(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
                                'user_id, date, time, order_quantity,'
                                'amount INTEGER DEFAULT 0,'
                                'ready INTEGER DEFAULT 0,'
                                'issued INTEGER DEFAULT 0)')
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
                x = self.cursor.execute("SELECT category FROM stock WHERE count >= 1 AND value = 1 AND country = ?",
                                        (counter,)).fetchall()
                return [i[0] for i in x]
        except IndexError:
            return []

    def bd_checks_for_category_product_in_stock(self, counter, category):
        """Отдаёт user список продуктов по стране и категории если продукт в наличии (количество более 1 шт)
        и флаг value = 1"""
        try:
            with self.connection:
                return self.cursor.execute("SELECT * FROM stock "
                                           "WHERE country = ? AND category = ? AND count >= 1 AND value = 1",
                                           (counter, category)).fetchall()
        except IndexError:
            return []

    def bd_returns_one_item(self, id_product):
        """Возращает полное описание одного товара по id товара"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM stock WHERE ID = ?", (id_product,)).fetchone()

    def bd_returns_one_item_price(self, id_product):
        """Возращает цену одного товара по id товара"""
        with self.connection:
            return self.cursor.execute("SELECT price FROM stock WHERE ID = ?", (id_product,)).fetchone()[0]
    def bd_returns_one_item_product_name(self, id_product):
        """Возращает product_name одного товара по id товара"""
        with self.connection:
            return self.cursor.execute("SELECT product_name FROM stock WHERE ID = ?", (id_product,)).fetchone()[0]

    def bd_order_verification(self, id_products):
        """Возращает полное описание одного товара по id товара"""
        a = []
        with self.connection:
            for i in id_products:
                print(int(i))
                a.append(self.cursor.execute("SELECT * FROM stock WHERE ID = ?", (i,)).fetchone())
            return a

    def bd_checks_product_in_the_basket(self, user_id, id_product):
        """проверка наличия товара в корзине"""
        print('22', user_id, id_product)
        with self.connection:
            return self.cursor.execute("SELECT count FROM basket WHERE user_id = ? AND id_product = ?",
                                       (user_id, id_product)).fetchall()

    def bd_all_product_for_user_in_the_basket(self, user_id):
        """DВозвращает все товары пользователя в корзине по ID"""
        with self.connection:
            all_product_for_user = self.cursor.execute("SELECT * FROM basket WHERE user_id = ?",
                                                       (user_id,)).fetchall()
            return all_product_for_user

    def bd_product_for_user_in_the_basket_availability(self, user_id):
        """Возвращает проверенные в наличии товары пользователя в корзине по ID"""
        with self.connection:
            all_product_for_user = self.cursor.execute("SELECT * FROM basket WHERE user_id = ? AND verified = 1",
                                                       (user_id,)).fetchall()
            return all_product_for_user

    def bd_checks_the_existence_of_the_user(self, user_id):
        """Проверка существования юзера в базе при старте бота"""
        with self.connection:
            return bool(
                self.cursor.execute("SELECT EXISTS(SELECT * FROM users WHERE user_id = ?)", (user_id,)).fetchone()[0])

    def bd_id_order(self, id_user):
        """Возвращает последний заказ"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM orders WHERE  user_id = ? GROUP BY user_id HAVING max(ID)", (id_user,)).fetchone()
    """*********************************************************************************"""

    """*********************Изменение значений в существующих записях ********************************************"""

    def bd_changes_count_in_basket(self, user_id, id_product):
        """Изменение количества товара в корзине yf +1"""
        with self.connection:
            self.cursor.execute(
                "UPDATE basket SET count = count + 1, count_stock = count_stock + 1 "
                "WHERE user_id = ? AND id_product = ?",
                (user_id, id_product))
            self.connection.commit()

    def bd_changes_count_in_basket_count_stock(self, id_user):
        """уравнивание корзины с наличием"""
        with self.connection:
            self.cursor.execute("UPDATE basket SET count = count_stock WHERE user_id = ?", (id_user,))
            self.connection.commit()

    def bd_changes_count_in_stock(self, index, id_product):
        """Изменение количества товара на складе"""
        with self.connection:
            self.cursor.execute(
                "UPDATE stock SET count = count - ? "
                "WHERE ID = ?",
                (index, id_product))
            self.connection.commit()

    def bd_del_from_the_basket(self, index, user_id, id_product):
        """Удаление одного товара из корзины"""
        if index == 0:
            with self.connection:
                self.cursor.execute("DELETE FROM basket WHERE user_id = ? AND id_product = ?",
                                    (user_id, id_product))
        else:
            with self.connection:
                self.cursor.execute("UPDATE basket SET count = count - ? WHERE user_id = ? AND id_product = ?",
                                    (index, user_id, id_product))
        self.connection.commit()

    def bd_checking_availability(self, count_stock, verified, user_id, id_product):
        """Изменяет количаство товара если в наличии меньше чем в корзине или нет в наличии,
        и изменяет статус проверено наличие
        count_stock - совпадает с количчеством товара в корзине если в наличии больше
        или становиться равным наличию,
        verified - , user_id, id_product"""
        with self.connection:
            self.cursor.execute("UPDATE basket SET count_stock = ?,"
                                " verified = ? "
                                "WHERE user_id = ? AND id_product = ?",
                                (count_stock, verified, user_id, id_product))
        self.connection.commit()

    def bd_del_all_basket_from_user(self, user_id):
        """удаление всех товаров пользователя"""
        with self.connection:
            self.cursor.execute("DELETE FROM basket WHERE user_id = ?", (user_id,))
        self.connection.commit()

    def bd_del_from_the_basket_no_verified(self, user_id):
        """Удаление товаров из корзины которых нет в наличии"""
        with self.connection:
            self.cursor.execute("DELETE FROM basket WHERE user_id = ? AND verified = 0",
                                (user_id,))



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
        """Запись товара добавленогов корзину но не купленого если есть в корзине то увеличивает количество"""

        if bool(len(self.bd_checks_product_in_the_basket(user_id, id_product))):
            self.bd_changes_count_in_basket(user_id, id_product)
        else:
            with self.connection:
                self.cursor.execute("INSERT INTO basket (user_id, id_product, count, count_stock) VALUES (?, ?, ?, ?)",
                                    (user_id, id_product, count, count))
                self.connection.commit()

    def bd_add_new_user(self, user_id, user_name, reg_date):
        """запись нового пользователя после нажатия старт"""
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id, user_name, reg_date) VALUES (?, ?, ?)",
                                (user_id, user_name, reg_date))
            self.connection.commit()

    def bd_add_product_in_orders(self, product):
        with self.connection:
            self.cursor.execute("INSERT INTO orders "
                                "(user_id, date, time, order_quantity, amount) VALUES (?, ?, ?, ?, ?)", product)
            self.connection.commit()

    '''*********************************************************************************'''

#
# db = DataBase('database.db')
# db.bd_add_product_in_basket(22, 55)
# #db.changes_count_in_basket(22, 55)
# db.bd_ad_new_user(1112, 'qwe', '12.09.23')
# db.bd_ad_new_user(11, 'q', '12.09.23')
# print(db.bd_checks_the_existence_of_the_user(11))
