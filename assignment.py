from decimal import Decimal


class InventoryItem:
    """Класс, в котором описывается сущность товара(предмета, id, title и цен."""

    """А также её id, title и цена"""

    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.price = Decimal("0.00")

    def __str__(self):
        return f"Товар: {self.title} (ID: {self.id}), Цена: {self.price} руб."


class Storage:
    """Класс, в котором описывается сущность склада, а также"""

    """его id, имя владельца и количество товаров"""

    def __init__(self, id, owner_name):
        self.id = id
        self.owner = owner_name
        self.items_count = 0

    def __str__(self):
        return f"Склад {self.id}"
        f"(Владелец: {self.owner}): {self.items_count} шт."


class InventoryOperation:
    """Родительский класс, в котором находятся методы-заглушки,"""

    """переопределяемые в дочерних классах"""

    def execute(self, item, *args):
        pass

    def undo(self, item, *args):
        pass


class AddItem(InventoryOperation):
    """Дочерний класс, в котором описана операция добавления предмета на склад,"""

    """также добавлена возможность отмены"""

    def execute(self, item, storage, amount):
        storage.items_count += amount
        print(f"Добавлено {amount} шт. Склад: {storage.id}")

    def undo(self, item, storage, amount):
        storage.items_count -= amount
        print(f"Отмена: списано {amount} шт. со склада {storage.id}")


class RemoveItem(InventoryOperation):
    """Дочерний класс, в котором описана операция удаления предмета со склада,"""

    """также добавлена возможность отмены"""

    def execute(self, item, storage, amount):
        if storage.items_count >= amount:
            storage.items_count -= amount
            print(f"Удалено {amount} шт. со склада {storage.id}")
        else:
            print("Ошибка: недостаточно товара для удаления")

    def undo(self, item, storage, amount):
        storage.items_count += amount
        print(f"Отмена: вернули {amount} шт. на склад {storage.id}")


class TransferItem(InventoryOperation):
    """Дочерний класс, в котором описана отправки предмета с одного склада на другой,"""

    """также добавлена возможность отмены"""

    def execute(self, item, source_storage, target_storage, amount):
        if source_storage.items_count >= amount:
            source_storage.items_count -= amount
            target_storage.items_count += amount
            print(
                f"Перемещено {amount} шт. со склада "
                f"{source_storage.id} на {target_storage.id}"
            )
        else:
            print("Ошибка: недостаточно товара для перемещения")

    def undo(self, item, source_storage, target_storage, amount):
        target_storage.items_count -= amount
        source_storage.items_count += amount
        print(
            "Отмена: Товар перемещен обратно "
            f"со склада {target_storage.id} на {source_storage.id}"
        )


class AdjustPrice(InventoryOperation):
    """Дочерний класс, в котором описана операция изменения цены, также добавлена возможность отмены"""

    def __init__(self):
        self.prev_price = None

    def execute(self, item, new_price):
        self.prev_price = item.price
        item.price = Decimal(str(new_price))
        print(f"Цена изменена с {self.prev_price} на {item.price}")

    def undo(self, item, *args):
        item.price = self.prev_price
        print(f"Отмена: Цене товара {item.title} возвращено значение {item.price}")


class InventoryManager:
    """Класс-обработчик, использующий принцип полиморфизма, т.е."""

    """он принимает любую операцию из вышеописанных и возвращает"""
    """результат метода и историю"""

    def __init__(self):
        self.history = []

    def execute_operation(self, operation, *args):
        operation.execute(*args)
        self.history.append((operation, args))

    def undo(self):
        if not self.history:
            print("История пуста, отменять нечего.")
            return

        operation, args = self.history.pop()
        operation.undo(*args)


manager = InventoryManager()


iphone = InventoryItem("101", "iPhone 15")
sklad_ivan = Storage("MSK-01", "Иван Иванов")
sklad_petr = Storage("SPB-02", "Петр Петров")


manager.execute_operation(AddItem(), iphone, sklad_ivan, 50)


price_cmd = AdjustPrice()
manager.execute_operation(price_cmd, iphone, 99000.50)


manager.execute_operation(TransferItem(), iphone, sklad_ivan, sklad_petr, 10)

print("Текущее состояние:")
print(sklad_ivan)
print(sklad_petr)
print(iphone)

print("Отмена двух последних действий:")
manager.undo()
manager.undo()

print("Итоговое состояние:")
print(sklad_ivan)
print(iphone)
