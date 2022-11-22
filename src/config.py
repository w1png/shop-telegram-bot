from json import loads, dump
from os import remove

filename = "config.json"
class Config:
    def __repr__(self):
        return self.__data 

    def __iter__(self):
        return self.__data

    def __getitem__(self, item):
        return self.__data[item]

    def __str__(self) -> str:
        return self.__raw 

    @property
    def __raw(self) -> str:
        with open(filename, "r") as f:
            return f.read()

    @property
    def __data(self):
       return loads(self.__raw) 

    def set(self, param: str, value: str | int) -> None:
        modified_data = self.__data
        modified_data[param] = value

        remove(filename)
        with open(filename, "w") as f:
            dump(modified_data, f, indent=2)

    def init(self) -> None:
        with open(filename, "w") as f:
            data = {
                "language": "ru",
                "shop_greeting": "Приветствуем в нашем магазине!",
            }
            dump(data, f, indent=2)
    
config = Config()


