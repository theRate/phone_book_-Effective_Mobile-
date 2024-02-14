from extensions import PhoneBook


def start():
    """Функция запускает главное меню программы телефонного справочника,
    отлавливает ошибки ввода со стороны пользователя."""

    phone_book = PhoneBook()

    while True:
        book_menu: str = input(
            "\n---- МЕНЮ СПРАВОЧНИКА ----\n"
            "  1. Показать весь справочник\n"
            "  2. Добавить новую запись\n"
            "  3. Редактировать запись\n"
            "  4. Найти запись\n"
            "  5. Выйти из справочника\n\n"
            "Выберите пункт меню (введите номер): "
        )

        if book_menu not in '12345':
            print("\nУпс! Введите номер соответствующего меню (1-5)")
            continue

        match book_menu:
            case '1':
                print('\n=> Вы выбрали "Показать весь справочник"')
                print('Телефонный справочник:')
                phone_book.display_contacts()
            case '2':
                while True:
                    print('\n=> Вы выбрали "Добавить новую записиь"')
                    try:
                        phone_book.add_contact()
                        break
                    except Exception as e:
                        print(e)
            case '3':
                while True:
                    print('\n=> Вы выбрали "Редактировать запись"')
                    try:
                        phone_book.edit_contact()
                        break
                    except Exception as e:
                        print(e)
            case '4':
                print('\n=>Вы выбрали "Найти запись"')
                phone_book.search_contacts()
            case '5':
                print('\n=> Вы выбрали "Выйти из справочника"')
                break


start()
