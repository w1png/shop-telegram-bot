import json
import constants

class PaymentMethod:
    def __init__(self, id: str) -> None:
        self.id = id
    
    def __str__(self) -> str:
        return f"[{self.id}] {self['title']}"

    def __repr__(self) -> str:
        return f"[{self.id}] {self['title']}"

    def __get_data(self) -> dict:
        return constants.config["payment_methods"][self.id]

    def __getitem__(self, key: str) -> str:
        return self.__get_data()[key]


def get_all_payment_methods() -> list[PaymentMethod]:
    # with open("payment_methods.json", "r") as file:
    #     result = []
    #     for id, data in json.loads(file.read()).items():
    #         if data["enabled"]:
    #             result.append(PaymentMethod(id))
    #     return result
    return [PaymentMethod(id) for id, data in constants.config["payment_methods"].items() if data["enabled"]]

