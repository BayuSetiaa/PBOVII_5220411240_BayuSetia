import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host='127.0.0.1',
            port='8889',
            user='root',
            password='root',
            database='5220411240'
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, data=None):
        try:
            if data:
                self.cursor.execute(query, data)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def fetch_data(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def close_connection(self):
        self.cursor.close()
        self.connection.close()


class CRUDProgram:
    def __init__(self, database):
        self.db = database

    def create_user(self, name, age):
        query = "INSERT INTO users (name, age) VALUES (%s, %s)"
        data = (name, age)
        self.db.execute_query(query, data)

    def update_user(self, user_id, new_name, new_age):
        query = "UPDATE users SET name = %s, age = %s WHERE id = %s"
        data = (new_name, new_age, user_id)
        self.db.execute_query(query, data)

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE id = %s"
        data = (user_id,)
        self.db.execute_query(query, data)

    def show_users(self):
        query = "SELECT * FROM users"
        result = self.db.fetch_data(query)
        if result:
            for row in result:
                print(row)
        else:
            print("No users found.")

    def create_product(self, name, price):
        query = "INSERT INTO products (name, price) VALUES (%s, %s)"
        data = (name, price)
        self.db.execute_query(query, data)

    def update_product(self, product_id, new_name, new_price):
        query = "UPDATE products SET name = %s, price = %s WHERE id = %s"
        data = (new_name, new_price, product_id)
        self.db.execute_query(query, data)

    def delete_product(self, product_id):
        query = "DELETE FROM products WHERE id = %s"
        data = (product_id,)
        self.db.execute_query(query, data)

    def show_products(self):
        query = "SELECT * FROM products"
        result = self.db.fetch_data(query)
        if result:
            for row in result:
                print(row)
        else:
            print("No products found.")

    def create_order(self, user_id, product_id, quantity, order_date):
        query = "INSERT INTO orders (user_id, product_id, quantity, order_date) VALUES (%s, %s, %s, %s)"
        data = (user_id, product_id, quantity, order_date)
        self.db.execute_query(query, data)
    
    def delete_order(self, order_id):
        query = "DELETE FROM orders WHERE id = %s"
        data = (order_id,)
        self.db.execute_query(query, data)

    def show_orders(self):
        query = "SELECT * FROM orders"
        result = self.db.fetch_data(query)
        if result:
            for row in result:
                print(row)
        else:
            print("No orders found.")

def main():
    db = Database(host="localhost", user="root", password="root", database="5220411240")

    db.execute_query("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT)")
    db.execute_query("CREATE TABLE IF NOT EXISTS products (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), price DECIMAL(10, 2))")
    db.execute_query("CREATE TABLE IF NOT EXISTS orders (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, product_id INT, quantity INT, order_date DATE, FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (product_id) REFERENCES products(id))")

    program = CRUDProgram(db)

    while True:
        print("\n1. Tambah User")
        print("2. Ubah User")
        print("3. Hapus User")
        print("4. Tampilkan Users")
        print("5. Tambah Product")
        print("6. Ubah Product")
        print("7. Hapus Product")
        print("8. Tampilkan Products")
        print("9. Tambah Order")
        print("10. Tampilkan Orders")
        print("11. Hapus Orders")
        print("0. Keluar")

        choice = input("Pilih operasi : ")

        if choice == "1":
            name = input("Masukkan nama user: ")
            age = int(input("Masukkan usia user: "))
            program.create_user(name, age)
        elif choice == "2":
            user_id = int(input("Masukkan ID user yang akan diubah: "))
            new_name = input("Masukkan nama baru: ")
            new_age = int(input("Masukkan usia baru: "))
            program.update_user(user_id, new_name, new_age)
        elif choice == "3":
            user_id = int(input("Masukkan ID user yang akan dihapus: "))
            program.delete_user(user_id)
        elif choice == "4":
            program.show_users()
        elif choice == "5":
            name = input("Masukkan nama product: ")
            price = float(input("Masukkan harga product: "))
            program.create_product(name, price)
        elif choice == "6":
            product_id = int(input("Masukkan ID product yang akan diubah: "))
            new_name = input("Masukkan nama baru: ")
            new_price = float(input("Masukkan harga baru: "))
            program.update_product(product_id, new_name, new_price)
        elif choice == "7":
            product_id = int(input("Masukkan ID product yang akan dihapus: "))
            program.delete_product(product_id)
        elif choice == "8":
            program.show_products()
        elif choice == "9":
            user_id = int(input("Masukkan ID user untuk pesanan: "))
            product_id = int(input("Masukkan ID product untuk pesanan: "))
            quantity = int(input("Masukkan jumlah pesanan: "))
            order_date = input("Masukkan tanggal pesanan (YYYY-MM-DD): ")
            program.create_order(user_id, product_id, quantity, order_date)
        elif choice == "10":
            program.show_orders()
        elif choice == "11":
            order_id = int(input("Masukkan ID order yang akan dihapus: "))
            program.delete_order(order_id)
        elif choice == "0":
            break
        else:
            print("Pilihan tidak valid. Silakan pilih lagi.")

    db.close_connection()
    print("Program selesai.")

if __name__ == "__main__":
    main()
