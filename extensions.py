import os
import csv


class ContactFieldDescription:
    """Дескриптор данных для проверки правильности заполнения текстовых полей в контактах.
    Так же пригодится при дальнейшем расширении функционала программы."""

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value: str):
        # Немного форматируем пользовательский ввод
        value = value.strip().capitalize()
        # Проверим, что строка состоит минимум из 1 символа (не пустое поле).
        if len(value) == 0:
            raise TypeError('\nКонтакт не добавлен! Текстовые поля не должны быть пустыми!')

        setattr(instance, self.name, value)


class ContactNumberDescription:
    """Дескриптор данных для проверки правильности заполнения полей с номерами в контактах.
    Так же пригодится при дальнейшем расширении функционала программы."""

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value: str):
        # Проверим, что номер записан цифрами и поле не пустое.
        if not value.isdigit() or len(value) == 0:
            raise TypeError('\nКонтакт не добавлен! Номера телефонов должны быть из цифр!')

        setattr(instance, self.name, value)


class Contact:
    """Класс контакта.
    Для удобного описания, создания, проверки контакта, и дальнейшего расширения функционала программы."""

    last_name = ContactFieldDescription()
    first_name = ContactFieldDescription()
    middle_name = ContactFieldDescription()
    organization = ContactFieldDescription()
    work_phone = ContactNumberDescription()
    personal_phone = ContactNumberDescription()

    def __init__(self, last_name, first_name, middle_name, organization, work_phone, personal_phone):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.organization = organization
        self.work_phone = work_phone
        self.personal_phone = personal_phone

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name} ({self.organization}):   " \
               f"рабочий телефон: {self.work_phone}, личный телефон: {self.personal_phone}"


class PhoneBook:
    """Класс телефонного справочника. Выполняет требуемые операции над справочником и контактами,
    которые присутствуют в меню справочника."""

    def __init__(self):
        self.file_name = 'my_phone_book.csv'

        # Проверяем наличие файла справочника
        if not os.path.isfile("my_phone_book.csv"):
            # Создаем файл при отсутствии
            with open("my_phone_book.csv", "w") as file:
                pass  # Просто пустой блок кода, нам нужен только фаил

    def display_contacts(self):
        """Метод выводит содержимое справочника на дисплей."""

        with open(self.file_name, 'r') as csvfile:
            # Читаем содержимое файла с помощью модуля csv
            csvreader = csv.reader(csvfile)
            # Выводим файл построчно
            for row in csvreader:
                cont = Contact(*row)
                print(cont)

    def add_contact(self):
        """Метод добавляет контакт в справочник."""

        # Создаем контакт для для дальнейшей записи в справочник
        contact = Contact(
            input('Введите фамилию: '),
            input('Введите имя: '),
            input('Введите отчество: '),
            input('Введите название организации: '),
            input('Введите рабочий телефон (только цифры): '),
            input('Введите личный телефон (только цифры): '),
        )

        # Добавление новой записи в справочник и сохранение ее в файле
        with open(self.file_name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(contact.__dict__.values())
            print(f'Добавлен контакт:  {contact}')

    def edit_contact(self):
        """Метод позволяет редактировать контакт.
        Для выбора контакта пользователю необходимо указать фамилию и имя."""

        query: str = input('Введите фамилию и имя для редактирования контакта: ')
        if len(query.split()) == 2:
            last_name, first_name = query.split()
        else:
            raise Exception('Ошибка ввода! Введите фамилию и имя через пробел!')

        # Читаем справочник
        with open(self.file_name, 'r') as csvfile:
            reader = csv.reader(csvfile)
            contacts = list(reader)

        # Проходим по справочнику, при обнаружении нужного контакта запрашиваем новую информацию по нему
        for contact in contacts:
            if contact[0].lower() == last_name.lower() and contact[1].lower() == first_name.lower():
                cont = Contact(
                    input('Введите новую фамилию: '),
                    input('Введите новое имя: '),
                    input('Введите новое отчество: '),
                    input('Введите новую организацию: '),
                    input('Введите новый рабочий телефон (только цифры): '),
                    input('Введите новый личный телефон (только цифры): '),
                )

                # Изменяем контактные данные на новые
                for i in range(6):
                    contact[i] = list(cont.__dict__.values())[i]

                # Перезаписываем справочник с измененным контактом
                with open(self.file_name, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(contacts)
                    print(f'Котакт успешно отредактирован: {cont}')
                break

            else:
                raise Exception('Контакта с такими фамилией и именем нет! Попробуйте еще раз!')

    def search_contacts(self):
        """Метод осуществляет поиск по справочнику по слову или набору цифр."""

        query: str = input('Введите слово или номер для поиска среди контактов: ')

        # Читаем файл
        with open(self.file_name, 'r') as file:
            reader = csv.reader(file)
            res = False

            # Ищем совпадения в контактах, выводим контакты с совпадением или инфу, что не нашли
            for row in reader:
                for item in row:
                    if query.lower() in item.lower():
                        print(Contact(*row))
                        res = True
                        break

            if not res:
                print(f'По вашему запросу "{query}" ничего не найдено!')
