import json
import random
import string
from pathlib import Path


class Bank:
    database = 'data.json'
    data = []

    @classmethod
    def __load_data(cls):
        
        if Path(cls.database).exists():
            with open(cls.database, 'r') as fs:
                try:
                    cls.data = json.load(fs)
                except json.JSONDecodeError:
                    cls.data = []
        else:
            cls.data = []

    @classmethod
    def __update(cls):
        
        with open(cls.database, 'w') as fs:
            json.dump(cls.data, fs, indent=4)

    @classmethod
    def __account_generate(cls):
        
        alpha = random.choice(string.ascii_letters)
        num = ''.join(random.choices(string.digits, k=3))
        spchar = random.choice("!@#$%^&*")
        id = list(alpha + num + spchar)
        random.shuffle(id)
        return "".join(id)

    def __init__(self):
        Bank.__load_data()

    def create_account(self, name, age, email, pin):
        if age < 18 or len(str(pin)) != 4:
            return {"status": False, "msg": "Must be 18+ and PIN must be 4 digits."}

        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": int(pin),
            "account_no": Bank.__account_generate(),
            "balance": 0,
        }

        Bank.data.append(info)
        Bank.__update()

        return {"status": True, "account_no": info['account_no']}

    def deposit_money(self, acc_number, pin, amount):
        self.__load_data()
        userdata = [i for i in Bank.data if i.get('account_no') == acc_number and i.get('pin') == int(pin)]


        if not userdata:
            return {"status": False, "msg": "Account not found or wrong PIN."}

        if not (0 < amount <= 10000):
            return {"status": False, "msg": "Amount must be between 1 and 10000."}

        userdata[0]['balance'] += amount
        Bank.__update()
        return {"status": True, "msg": "Deposit successful!"}

    def withdraw_money(self, acc_number, pin, amount):
        self.__load_data()
        userdata = [i for i in Bank.data if i.get('account_no') == acc_number and i.get('pin') == int(pin)]


        if not userdata:
            return {"status": False, "msg": "Account not found or wrong PIN."}

        if userdata[0]['balance'] < amount:
            return {"status": False, "msg": "Insufficient balance."}

        userdata[0]['balance'] -= amount
        Bank.__update()
        return {"status": True, "msg": "Withdrawal successful!"}

    def show_details(self, acc_number, pin):
        self.__load_data()
        userdata = [i for i in Bank.data if 'account_no' in i and 'pin' in i and i['account_no'] == acc_number and i['pin'] == int(pin)]

        return userdata[0] if userdata else None

    def update_details(self, acc_number, pin, new_name=None, new_email=None, new_pin=None):
        self.__load_data()
        userdata = [i for i in Bank.data if i.get('account_no') == acc_number and i.get('pin') == int(pin)]


        if not userdata:
            return {"status": False, "msg": "Account not found or wrong PIN."}

        if new_name:
            userdata[0]['name'] = new_name
        if new_email:
            userdata[0]['email'] = new_email
        if new_pin:
            if len(str(new_pin)) == 4:
                userdata[0]['pin'] = int(new_pin)
            else:
                return {"status": False, "msg": "PIN must be exactly 4 digits."}

        Bank.__update()
        return {"status": True, "msg": "Details updated successfully!"}

    def delete_account(self, acc_number, pin):
        self.__load_data()
        userdata = [i for i in Bank.data if i['account_no'] == acc_number and i['pin'] == int(pin)]

        if not userdata:
            return {"status": False, "msg": "Account not found or wrong PIN."}

        Bank.data.remove(userdata[0])
        Bank.__update()
        return {"status": True, "msg": "Account deleted successfully!"}



