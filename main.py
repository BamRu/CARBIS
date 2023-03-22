import sys
sys.path.insert(1,"Lib")
from dadata import Dadata
import sqlite3
import os

user = None

def GetCoordinates(data):
    os.system('cls')
    dadata = Dadata(user[1], user[2])
    try:
        #result = dadata.suggest(name="address", query=data, language=user[3])
        cord = dadata.clean(name="address", source=data)
        print("Адрес: ", data)
        if cord["geo_lat"] or cord["geo_lon"] is not None:
            print("Широта:", cord["geo_lat"], "Долгота:", cord["geo_lon"])
        else:
            print("Не удалось найти координаты в базе dadata")
    except:
        os.system('cls')
        print("Ошибка при работе с dadata проверьте API и секретный ключ")
        return KeyError;

def AddressClarification(data):
    dadata = Dadata(user[1])
    try:
        result = dadata.suggest(name="address", query=data, language=user[3])
    except:
        os.system('cls')
        print("Ошибка при работе с dadata проверьте API-ключ")
        return KeyError;
    if len(result) == 0:
        print("Не удалось найти адрес пожалуйста уточните детали")
        return;
    if len(result) == 1:
        return result[0]["value"]
    for i, unit in zip(range(1,len(result)+1),result):
        print(i,unit["value"])
    while(True):
        try:
            choise = int(input("Введите номер нужного вам адреса. Если адреса нет в списке введите 0 и попробуйте уточнить детали:"))
            if choise > 0 and choise <= len(result):
                print (result[(choise)-1]["value"])
                return (result[(choise)-1]["value"])
            elif choise == 0:
                break;
            else:
                print ("Неверно введено число. Попробуйте еще раз ")
        except ValueError:
            print("Введите номер из списка")
    return ;

def Registration():
    os.system('cls')
    try:
        db = sqlite3.connect("usersettings.db")
        cursor = db.cursor()

        query ="""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            name VARCHAR(30),
            api_key VARCHAR(30),
            secret_key VARCHAR(30),
            lang VARCHAR(2)
        );
        """
        cursor.executescript(query)
        while (True):
            name = input("Логин: ")
            cursor.execute("SELECT name FROM users where name = ?", [name])

            if name == "": break

            if cursor.fetchone() is None:

                api_key = input("API ключ: ")
                secret_key = input("Секретный ключ: ")
                while (True):
                    lang = str.lower(input("Выберете язык из предложенных ( ru / en ): "))
                    if lang == "ru" or lang == "en":
                        break
                    print("Язык введен некоректно")

                global user
                user = [name, api_key ,secret_key, lang]
                cursor.execute("INSERT INTO users(name, api_key, secret_key, lang) VALUES(?, ?, ?, ?)", user)
                db.commit()
                break;
            else:
                print("Такой логин уже занят, введите пожалуйста другой (Для выхода в главное меню оставьте поле пустым и нажмите enter):")


    except sqlite3.Error as e:
        print("Error", e)
    finally:
        cursor.close()
        db.close()


def Join():
    os.system('cls')
    try:
        db = sqlite3.connect("usersettings.db")
        cursor = db.cursor()
        if cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='users'""").fetchall() == []:
            print("В базе данных нет зарегистрированных пользователей. Будьте первым кто создаст профиль!!")
        else:
            while(True):
                name = input("Для входа введите имя пользователя: ")
                if name == "": break
                cursor.execute("SELECT name, api_key, secret_key, lang FROM users WHERE name = ?", [name])
                global user
                user = cursor.fetchone();
                if user is not None:
                    break
                else:
                    os.system('cls')
                    print("Имя введено некорректно попробуйте войти еще раз или зарегистрируйтесь в главном меню. (Для выхода в главное меню оставьте поле пустым и нажмите enter)")

    except sqlite3.Error as e:
        print("Error", e)
    finally:
        cursor.close()
        db.close()

def InputAddress():
    while (True):

        data = input("Введите адрес для поиска(Для выхода оставьте поле пустым и нажмите enter): ")
        if data != "":
            address = AddressClarification(data)
            if address is KeyError:
                break
            if address is not None:
                GetCoordinates(address)
        else:
            break

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    os.system('cls')
    print("Для начала работы необходимо зарегистрироваться или войти.")
    while(user is None):
        print("Выберите действие (Введите номер пункта):")
        print("1 - зарегистрироваться")
        print("2 - войти")
        print("0 - выйти из программы")

        auth = input()

        try:
            if int(auth) == 1:
                Registration()
            elif int(auth) == 2:
                Join()
            elif int(auth) == 0:
                break
            else:
                os.system('cls')
                print("Введите номер пункта из списка!")
        except ValueError:
            os.system('cls')
            print("Введите число сопоставимое с действием из списка!")
    if user is not None:
        os.system('cls')
        InputAddress()

print("Досвидания")


