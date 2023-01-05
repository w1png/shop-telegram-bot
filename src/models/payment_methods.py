import json

class PaymentMethod:
    def __init__(self, id: str) -> None:
        self.id = id
    
    def __get_data(self) -> dict:
        with open("payment_methods.json", "r") as file:
            return json.loads(file.read())[self.id]

    def __getitem__(self, key: str) -> str:
        return self.__get_data()[key]


def get_all_payment_methods() -> list[PaymentMethod]:
    with open("payment_methods.json", "r") as file:
        return [PaymentMethod(id) for id in json.loads(file.read())]
    

