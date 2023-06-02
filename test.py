class BankAccount:
    def __init__(self, initial_balance):
        # 初期残高を設定
        self.balance = initial_balance

    def deposit(self, amount):
        # 残高に預金額を加算
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        # 引き出し額が残高を超えていないか確認
        if amount > self.balance:
            raise ValueError("残高不足")
        # 残高から引き出し額を減算
        self.balance -= amount
        return self.balance

    def check_balance(self):
        # 残高を返す
        return self.balance


class Customer:
    def __init__(self, name, bank_account):
        # 顧客名と銀行口座を設定
        self.name = name
        self.bank_account = bank_account

    def make_deposit(self, amount):
        # 顧客の口座に預金
        self.bank_account.deposit(amount)
        print(
            f"{self.name}さんが{amount}円預けました。新しい残高: {self.bank_account.check_balance()}円")

    def make_withdrawal(self, amount):
        # 顧客の口座から引き出し
        try:
            self.bank_account.withdraw(amount)
            print(
                f"{self.name}さんが{amount}円引き出しました。新しい残高: {self.bank_account.check_balance()}円")
        except ValueError:
            print(f"{self.name}さんの引き出しは残高不足です")

    def check_balance(self):
        # 顧客の口座残高を確認
        print(f"{self.name}さんの残高: {self.bank_account.check_balance()}円")


# 銀行口座を作成
alice_account = BankAccount(500)

# 顧客を作成
alice = Customer("アリス", alice_account)

# アリスが預ける
alice.make_deposit(200)

# アリスが引き出す
alice.make_withdrawal(100)

# アリスが残高を確認
alice.check_balance()
