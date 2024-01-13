import mysql.connector

# Fungsi untuk membuat koneksi ke database
def create_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port='8889',
        user="root",
        password="root",
        database=None  # Tidak menggunakan database pada saat inisialisasi
    )

# Fungsi untuk mengeksekusi pernyataan SQL
def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# Membuat koneksi ke MySQL tanpa menggunakan database
connection = create_connection()

# Mengeksekusi pernyataan SQL untuk membuat database jika belum ada
execute_query(connection, "CREATE DATABASE IF NOT EXISTS `5220411240`;")

# Menutup koneksi sementara
connection.close()

# Membuat koneksi ke database yang telah dibuat
connection = create_connection()
execute_query(connection, "USE `5220411240`;")

# Membuat koneksi ke database yang telah dibuat
connection = create_connection()
execute_query(connection, "USE `5220411240`;")

# Mengeksekusi pernyataan SQL untuk membuat tabel
execute_query(connection, """
    CREATE TABLE IF NOT EXISTS `users` (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `name` VARCHAR(255) NOT NULL,
        `age` INT
    );
""")

# Mengeksekusi pernyataan SQL untuk membuat tabel products
execute_query(connection, """
    CREATE TABLE IF NOT EXISTS `products` (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `name` VARCHAR(255) NOT NULL,
        `price` DECIMAL(10, 2) NOT NULL
    );
""")


# Mengeksekusi pernyataan SQL untuk membuat tabel orders
execute_query(connection, """
    CREATE TABLE IF NOT EXISTS `orders` (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `user_id` INT NOT NULL,
        `product_id` INT NOT NULL,
        `quantity` INT NOT NULL,
        `order_date` DATE NOT NULL,
        FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
        FOREIGN KEY (`product_id`) REFERENCES `products`(`id`)
    );
""")

# Menutup koneksi
connection.close()
