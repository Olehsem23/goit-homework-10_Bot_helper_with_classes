from Addressbook_classes import AddressBook, Name, Phone, Record

address_book = AddressBook()


def input_error(func):  # Декоратор. Обробляє помилки при вводі.
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return f"No user with name {args[0]}"
        except ValueError:
            return 'Give me name and phone please'
        except IndexError:
            return 'Enter user name and phone'
    return wrapper


@input_error
def hello_user():  # Відповідь на команду 'Hello'
    return "Hello! How can I help you?"


@input_error
def add_command(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone)
    return address_book.add_record(rec)


@input_error
def change_command(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact {name} in address book"


@input_error
def show_all_command():  # Видрукувати весь список імен і телефонів зі словника address_book.
    if len(address_book) == 0:  # Якщо словник порожній.
        return 'Address book is now empty. Please add some users'
    else:
        print(f'There are {len(address_book)} users in address book')
        return address_book


@input_error
def phone_command(*args):  # Пошук телефона вибраного користувача.
    return address_book[args[0]]


def exit_command():  # Вихід з програми.
    return 'Bye. Have a nice day. See you next time.'


def unknown_command():  # Коли вводимо невідому команду.
    return 'Unknown command. Try again'


# COMMANDS - словник, де ключі - це функції, які викликаються при наборі відповідної команди з кортежу можливих команд.
COMMANDS = {
    hello_user: ('hello', 'hi', 'aloha', 'привіт'),
    show_all_command: ('show all', 'all phones', 'addressbook', 'phonebook'),
    add_command: ('new user', 'add', '+'),
    change_command: ('change phone for', 'change', 'зміни', 'замінити'),
    phone_command: ('show number', 'phone', 'number', 'show'),
    exit_command: ('bye', 'exit', 'end', 'close', 'goodbye')
}


def parser(text: str):  # Парсер команд
    for cmd, keywords in COMMANDS.items():
        for kwd in keywords:
            if text.lower().startswith(kwd):
                # print(cmd)
                data = text[len(kwd):].strip().split()
                # print(data)
                return cmd, data 
    return unknown_command, []


def main():
    while True:
        user_input = input('Enter your command and args: ')
        
        cmd, data = parser(user_input)
        
        result = cmd(*data)
        
        print(result)
        
        if cmd == exit_command:  # Вихід з бота
            break


if __name__ == "__main__":  # Точка входження
    main()
