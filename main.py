import json
import os
import random
from collections import deque
from abc import ABC, abstractmethod
from datetime import datetime


# ==================== Модель задачи ====================
class Task(ABC):
    """Абстрактный базовый класс для всех задач"""

    def __init__(self, description, difficulty):
        self._description = description  # Инкапсуляция
        self._type = self.get_type()
        self._difficulty = difficulty
        self._created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @abstractmethod
    def get_type(self):
        """Возвращает тип задачи (полиморфизм)"""
        pass

    @property
    def description(self):
        return self._description

    @property
    def task_type(self):
        return self._type

    @property
    def difficulty(self):
        return self._difficulty

    @property
    def created_at(self):
        return self._created_at

    def to_dict(self):
        """Конвертация в словарь для JSON"""
        return {
            "description": self._description,
            "type": self._type,
            "difficulty": self._difficulty,
            "created_at": self._created_at
        }

    def __str__(self):
        difficulty_icon = {1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐"}.get(self._difficulty, "⭐")
        return f"[{self._type.upper()}] {difficulty_icon} {self._description} (Сложность: {self._difficulty}/3)"

    def display_full(self):
        """Полное отображение задачи"""
        border = "=" * 60
        return f"\n{border}\n📋 ЗАДАЧА\nТип: {self._type}\nОписание: {self._description}\nСложность: {self._difficulty}/3\nСоздана: {self._created_at}\n{border}"


# ==================== Конкретные типы задач ====================
class WorkTask(Task):
    """Рабочая задача"""

    def get_type(self):
        return "работа"


class SportTask(Task):
    """Спортивная задача"""

    def get_type(self):
        return "спорт"


class StudyTask(Task):
    """Учебная задача"""

    def get_type(self):
        return "учеба"


class HomeTask(Task):
    """Домашняя задача"""

    def get_type(self):
        return "дом"


class HealthTask(Task):
    """Задача о здоровье"""

    def get_type(self):
        return "здоровье"


# ==================== Factory Pattern ====================
class TaskFactory:
    """Фабрика для создания задач разных типов"""

    _task_types = {
        "работа": WorkTask,
        "спорт": SportTask,
        "учеба": StudyTask,
        "дом": HomeTask,
        "здоровье": HealthTask
    }

    @classmethod
    def create_task(cls, task_type, description, difficulty):
        """Создаёт задачу указанного типа"""
        task_class = cls._task_types.get(task_type.lower())
        if task_class:
            return task_class(description, difficulty)
        else:
            raise ValueError(f"Неизвестный тип задачи: {task_type}")

    @classmethod
    def get_available_types(cls):
        """Возвращает список доступных типов задач"""
        return list(cls._task_types.keys())


# ==================== Управление задачами ====================
class TaskManager:
    """Управление коллекцией задач"""

    def __init__(self, filename="tasks.json"):
        self._filename = filename
        self._tasks = []
        self._load_tasks()

    def _load_tasks(self):
        """Загрузка задач из JSON"""
        if os.path.exists(self._filename):
            try:
                with open(self._filename, 'r', encoding='utf-8') as f:
                    tasks_data = json.load(f)
                    for task_data in tasks_data:
                        task = TaskFactory.create_task(
                            task_data["type"],
                            task_data["description"],
                            task_data["difficulty"]
                        )
                        self._tasks.append(task)
                print(f"✅ Загружено {len(self._tasks)} задач")
            except Exception as e:
                print(f"❌ Ошибка загрузки: {e}")
                self._create_default_tasks()
        else:
            self._create_default_tasks()

    def _create_default_tasks(self):
        """Создание стандартных задач"""
        default_tasks = [
            ("работа", "Завершить отчёт по проекту", 2),
            ("работа", "Провести встречу с командой", 1),
            ("работа", "Подготовить презентацию", 3),
            ("спорт", "Сделать зарядку", 1),
            ("спорт", "Пробежать 5 км", 2),
            ("спорт", "Сходить в спортзал", 2),
            ("учеба", "Прочитать главу из книги", 1),
            ("учеба", "Изучить новый фреймворк", 3),
            ("учеба", "Решить 10 задач по программированию", 2),
            ("дом", "Убрать в комнате", 1),
            ("дом", "Приготовить ужин", 2),
            ("дом", "Сделать генеральную уборку", 3),
            ("здоровье", "Выпить 2 литра воды", 1),
            ("здоровье", "Провести медитацию", 1),
            ("здоровье", "Лечь спать вовремя", 2)
        ]

        for task_type, desc, difficulty in default_tasks:
            task = TaskFactory.create_task(task_type, desc, difficulty)
            self._tasks.append(task)

        self._save_tasks()
        print(f"📝 Создано {len(self._tasks)} стандартных задач")

    def _save_tasks(self):
        """Сохранение задач в JSON"""
        try:
            with open(self._filename, 'w', encoding='utf-8') as f:
                tasks_data = [task.to_dict() for task in self._tasks]
                json.dump(tasks_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            return False

    def add_task(self, task_type, description, difficulty):
        """Добавление новой задачи"""
        try:
            task = TaskFactory.create_task(task_type, description, difficulty)
            self._tasks.append(task)
            self._save_tasks()
            print(f"✅ Задача добавлена: {task}")
            return True
        except ValueError as e:
            print(f"❌ Ошибка: {e}")
            return False

    def get_tasks(self):
        """Получение всех задач"""
        return self._tasks.copy()

    def get_tasks_filtered(self, task_type=None, difficulty=None):
        """Фильтрация задач по типу и сложности"""
        filtered = self._tasks.copy()

        if task_type:
            filtered = [t for t in filtered if t.task_type == task_type]

        if difficulty is not None:
            filtered = [t for t in filtered if t.difficulty == difficulty]

        return filtered

    def get_random_task(self, task_type=None, difficulty=None):
        """Получение случайной задачи с учётом фильтров"""
        filtered = self.get_tasks_filtered(task_type, difficulty)

        if not filtered:
            return None

        return random.choice(filtered)

    def get_statistics(self):
        """Статистика по задачам"""
        stats = {
            "всего": len(self._tasks),
            "по_типам": {},
            "по_сложности": {1: 0, 2: 0, 3: 0}
        }

        for task in self._tasks:
            # По типам
            task_type = task.task_type
            stats["по_типам"][task_type] = stats["по_типам"].get(task_type, 0) + 1

            # По сложности
            stats["по_сложности"][task.difficulty] += 1

        return stats


# ==================== Очередь истории ====================
class HistoryQueue:
    """Очередь для хранения истории сгенерированных задач"""

    def __init__(self, max_size=50, filename="history.json"):
        self._queue = deque(maxlen=max_size)
        self._filename = filename
        self._load_history()

    def _load_history(self):
        """Загрузка истории из JSON"""
        if os.path.exists(self._filename):
            try:
                with open(self._filename, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                    for item in history_data:
                        self._queue.append(item)
                print(f"📜 Загружено {len(self._queue)} записей истории")
            except Exception as e:
                print(f"❌ Ошибка загрузки истории: {e}")

    def _save_history(self):
        """Сохранение истории в JSON"""
        try:
            with open(self._filename, 'w', encoding='utf-8') as f:
                json.dump(list(self._queue), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения истории: {e}")
            return False

    def add(self, task):
        """Добавление задачи в историю"""
        history_entry = {
            "task": task.to_dict(),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self._queue.append(history_entry)
        self._save_history()

    def get_all(self):
        """Получение всей истории"""
        return list(self._queue)

    def get_last(self, count=5):
        """Получение последних N задач"""
        items = list(self._queue)
        return items[-count:] if items else []

    def clear(self):
        """Очистка истории"""
        self._queue.clear()
        self._save_history()
        print("✅ История очищена")

    def get_size(self):
        """Размер очереди"""
        return len(self._queue)


# ==================== Валидатор ввода ====================
class InputValidator:
    """Класс для валидации пользовательского ввода"""

    @staticmethod
    def validate_description(description):
        """Проверка описания задачи"""
        if not description or not description.strip():
            return False, "Описание не может быть пустым"
        if len(description) > 200:
            return False, "Описание не должно превышать 200 символов"
        if len(description.strip()) < 3:
            return False, "Описание должно содержать минимум 3 символа"
        return True, description.strip()

    @staticmethod
    def validate_difficulty(difficulty_str):
        """Проверка сложности"""
        try:
            difficulty = int(difficulty_str)
            if difficulty not in [1, 2, 3]:
                return False, "Сложность должна быть 1, 2 или 3"
            return True, difficulty
        except ValueError:
            return False, "Введите число (1, 2 или 3)"

    @staticmethod
    def validate_task_type(task_type, available_types):
        """Проверка типа задачи"""
        if task_type.lower() not in available_types:
            return False, f"Доступные типы: {', '.join(available_types)}"
        return True, task_type.lower()

    @staticmethod
    def get_valid_input(prompt, validator_func, *args):
        """Получение и валидация ввода"""
        while True:
            user_input = input(prompt).strip()
            is_valid, result = validator_func(user_input, *args) if args else validator_func(user_input)
            if is_valid:
                return result
            print(f"❌ {result}")


# ==================== Основное приложение ====================
class RandomTaskGenerator:
    """Главный класс приложения"""

    def __init__(self):
        self.task_manager = TaskManager()
        self.history = HistoryQueue()
        self.available_types = TaskFactory.get_available_types()

    def display_menu(self):
        """Отображение главного меню"""
        print("\n" + "=" * 50)
        print("🎲 RANDOM TASK GENERATOR")
        print("=" * 50)
        print("1. 🎯 Сгенерировать случайную задачу")
        print("2. 📋 Показать все задачи")
        print("3. 🔍 Фильтрация задач")
        print("4. ➕ Добавить новую задачу")
        print("5. 📜 Показать историю")
        print("6. 📊 Статистика")
        print("7. 🗑 Очистить историю")
        print("0. 🚪 Выход")
        print("-" * 50)

    def display_filter_menu(self):
        """Отображение меню фильтрации"""
        print("\n🔍 ФИЛЬТРАЦИЯ ЗАДАЧ")
        print("1. По типу")
        print("2. По сложности")
        print("3. По типу и сложности")
        print("4. Сгенерировать с фильтрами")
        print("0. Назад")
        print("-" * 30)

    def generate_random_task(self, task_type=None, difficulty=None):
        """Генерация случайной задачи"""
        task = self.task_manager.get_random_task(task_type, difficulty)

        if task:
            print("\n" + "🎉" * 25)
            print(task.display_full())
            print("🎉" * 25)

            # Сохранение в историю
            self.history.add(task)
            print(f"\n✅ Задача сохранена в истории (всего: {self.history.get_size()})")
        else:
            print("\n❌ Нет задач, соответствующих критериям!")
            print("Попробуйте изменить фильтры или добавьте новые задачи")

        return task

    def show_all_tasks(self):
        """Показать все задачи"""
        tasks = self.task_manager.get_tasks()

        if not tasks:
            print("\n📭 Нет доступных задач")
            return

        print(f"\n📚 ВСЕ ЗАДАЧИ ({len(tasks)})")
        print("-" * 50)

        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")

    def filter_tasks(self):
        """Интерактивная фильтрация задач"""
        while True:
            self.display_filter_menu()
            choice = input("\nВыберите действие: ").strip()

            if choice == '1':
                # Фильтр по типу
                print(f"\nДоступные типы: {', '.join(self.available_types)}")
                task_type = InputValidator.get_valid_input(
                    "Введите тип задачи: ",
                    lambda x: InputValidator.validate_task_type(x, self.available_types)
                )

                filtered = self.task_manager.get_tasks_filtered(task_type=task_type)
                self._display_filtered_results(filtered, f"Тип: {task_type}")

            elif choice == '2':
                # Фильтр по сложности
                difficulty = InputValidator.get_valid_input(
                    "Введите сложность (1-3): ",
                    InputValidator.validate_difficulty
                )

                filtered = self.task_manager.get_tasks_filtered(difficulty=difficulty)
                self._display_filtered_results(filtered, f"Сложность: {difficulty}/3")

            elif choice == '3':
                # Фильтр по типу и сложности
                print(f"\nДоступные типы: {', '.join(self.available_types)}")
                task_type = InputValidator.get_valid_input(
                    "Введите тип задачи: ",
                    lambda x: InputValidator.validate_task_type(x, self.available_types)
                )

                difficulty = InputValidator.get_valid_input(
                    "Введите сложность (1-3): ",
                    InputValidator.validate_difficulty
                )

                filtered = self.task_manager.get_tasks_filtered(
                    task_type=task_type,
                    difficulty=difficulty
                )
                self._display_filtered_results(filtered, f"Тип: {task_type}, Сложность: {difficulty}/3")

            elif choice == '4':
                # Генерация с фильтрами
                print("\n🎲 ГЕНЕРАЦИЯ С ФИЛЬТРАМИ")
                print(f"Доступные типы: {', '.join(self.available_types)}")

                use_filter = input("Использовать фильтр по типу? (y/n): ").lower()
                task_type = None
                if use_filter == 'y':
                    task_type = InputValidator.get_valid_input(
                        "Введите тип задачи: ",
                        lambda x: InputValidator.validate_task_type(x, self.available_types)
                    )

                use_difficulty = input("Использовать фильтр по сложности? (y/n): ").lower()
                difficulty = None
                if use_difficulty == 'y':
                    difficulty = InputValidator.get_valid_input(
                        "Введите сложность (1-3): ",
                        InputValidator.validate_difficulty
                    )

                self.generate_random_task(task_type, difficulty)

            elif choice == '0':
                break

            else:
                print("❌ Неверный выбор")

    def _display_filtered_results(self, filtered_tasks, filter_criteria):
        """Отображение отфильтрованных результатов"""
        if not filtered_tasks:
            print(f"\n❌ Нет задач по критерию: {filter_criteria}")
            return

        print(f"\n✅ Найдено задач: {len(filtered_tasks)}")
        print(f"📌 Критерий: {filter_criteria}")
        print("-" * 50)

        for i, task in enumerate(filtered_tasks, 1):
            print(f"{i}. {task}")

    def add_new_task(self):
        """Добавление новой задачи"""
        print("\n➕ ДОБАВЛЕНИЕ НОВОЙ ЗАДАЧИ")
        print(f"Доступные типы: {', '.join(self.available_types)}")

        # Ввод и валидация типа
        task_type = InputValidator.get_valid_input(
            "Тип задачи: ",
            lambda x: InputValidator.validate_task_type(x, self.available_types)
        )

        # Ввод и валидация описания
        description = InputValidator.get_valid_input(
            "Описание задачи: ",
            InputValidator.validate_description
        )

        # Ввод и валидация сложности
        difficulty = InputValidator.get_valid_input(
            "Сложность (1-3): ",
            InputValidator.validate_difficulty
        )

        # Добавление задачи
        if self.task_manager.add_task(task_type, description, difficulty):
            print("\n💡 Совет: Теперь задача доступна для генерации!")

    def show_history(self):
        """Показать историю сгенерированных задач"""
        history_items = self.history.get_all()

        if not history_items:
            print("\n📭 История пуста")
            print("Сгенерируйте хотя бы одну задачу, чтобы увидеть историю")
            return

        print(f"\n📜 ИСТОРИЯ ГЕНЕРАЦИИ (всего: {len(history_items)})")
        print("=" * 60)

        for i, item in enumerate(reversed(history_items), 1):
            task_data = item["task"]
            generated_at = item["generated_at"]
            difficulty_icon = {1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐"}.get(task_data["difficulty"], "⭐")

            print(f"\n{i}. [{task_data['type'].upper()}] {difficulty_icon} {task_data['description']}")
            print(f"   📅 Сгенерирована: {generated_at}")
            print(f"   📊 Сложность: {task_data['difficulty']}/3")

        # Показать последние 5 задач
        print("\n" + "=" * 60)
        print("🆕 ПОСЛЕДНИЕ 5 ЗАДАЧ:")
        last_tasks = self.history.get_last(5)
        for task in reversed(last_tasks):
            task_data = task["task"]
            print(f"   • [{task_data['type']}] {task_data['description'][:50]}")

    def show_statistics(self):
        """Показать статистику"""
        task_stats = self.task_manager.get_statistics()

        print("\n📊 СТАТИСТИКА ЗАДАЧ")
        print("=" * 40)
        print(f"📚 Всего задач в базе: {task_stats['всего']}")

        print("\n📂 По типам:")
        for task_type, count in sorted(task_stats["по_типам"].items()):
            bar = "█" * min(count, 20)
            print(f"   {task_type.capitalize()}: {bar} {count}")

        print("\n⭐ По сложности:")
        for diff, count in task_stats["по_сложности"].items():
            stars = "⭐" * diff
            bar = "█" * min(count, 20)
            print(f"   {stars}: {bar} {count}")

        print(f"\n📜 Записей в истории: {self.history.get_size()}")

        if self.history.get_size() > 0:
            last_task = self.history.get_last(1)[0]
            task_data = last_task["task"]
            print(f"🆕 Последняя задача: [{task_data['type']}] {task_data['description'][:40]}")

    def clear_history(self):
        """Очистка истории с подтверждением"""
        confirm = input("\n⚠️ Вы уверены, что хотите очистить всю историю? (y/n): ").lower()
        if confirm == 'y':
            self.history.clear()
        else:
            print("❌ Очистка отменена")

    def run(self):
        """Запуск приложения"""
        print("\n🎲 Добро пожаловать в Random Task Generator!")
        print(f"📚 Доступно типов задач: {', '.join(self.available_types)}")

        while True:
            self.display_menu()
            choice = input("\nВыберите действие: ").strip()

            if choice == '1':
                self.generate_random_task()

            elif choice == '2':
                self.show_all_tasks()

            elif choice == '3':
                self.filter_tasks()

            elif choice == '4':
                self.add_new_task()

            elif choice == '5':
                self.show_history()

            elif choice == '6':
                self.show_statistics()

            elif choice == '7':
                self.clear_history()

            elif choice == '0':
                print("\n👋 До свидания! Продолжайте выполнять задачи!")
                break

            else:
                print("❌ Неверный выбор. Попробуйте снова")


# ==================== Точка входа ====================
def main():
    app = RandomTaskGenerator()
    app.run()


if __name__ == "__main__":
    main()
