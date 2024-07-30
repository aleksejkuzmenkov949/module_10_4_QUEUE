import threading
import time
import queue

class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False

class Customer(threading.Thread):
    def __init__(self, customer_id, cafe):
        super().__init__()
        self.customer_id = customer_id
        self.cafe = cafe

    def run(self):
        self.cafe.serve_customer(self)

class Cafe:
    def __init__(self, tables):
        self.tables = tables
        self.queue = queue.Queue()

    def customer_arrival(self):
        for customer_id in range(1, 21):  # Ограничение на 20 посетителей
            print(f'Посетитель номер {customer_id} прибыл.')
            customer = Customer(customer_id, self)
            customer.start()
            time.sleep(1)  # Приход новых посетителей каждую секунду

    def serve_customer(self, customer):
        for table in self.tables:
            if not table.is_busy:
                table.is_busy = True
                print(f'Посетитель номер {customer.customer_id} сел за стол {table.number}.')
                time.sleep(5)  # Время обслуживания
                table.is_busy = False
                print(f'Посетитель номер {customer.customer_id} покушал и ушёл.')
                return

        print(f'Посетитель номер {customer.customer_id} ожидает свободный стол.')
        self.queue.put(customer)  # Помещение в очередь, если нет свободного стола

# Создаем столики в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализируем кафе
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()

