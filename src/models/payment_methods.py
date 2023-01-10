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

    def set_enabled(self, enabled: bool) -> None:
        constants.config.set(("payment_methods", self.id), {"title": self["title"], "enabled": enabled})


def get_enabled_payment_methods() -> list:
    return [PaymentMethod(id) for id, data in constants.config["payment_methods"].items() if data["enabled"]]

def get_all_payment_methods() -> list[PaymentMethod]:
    return [PaymentMethod(id) for id in constants.config["payment_methods"]]
