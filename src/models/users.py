import asyncio
from typing import Any
import datetime
import json

import database
import constants


class User:
    def __init__(self, user_id: int) -> None:
        self.id = user_id
        
    @property
    def database_table(self) -> str:
        return """CREATE TABLE IF NOT EXISTS users (
            id INTEGER,
            is_admin INTEGER,
            is_manager INTEGER,
            notification INTEGER,
            date_created TEXT,
            cart TEXT
            )"""
    
    def __str__(self) -> str:
        return str(self.id)

    def __repr__(self) -> str:
        return str(self.id)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.id == other.id
        return False
    
    async def _query(self, field: str) -> Any:
        return (await database.fetch(f"SELECT {field} FROM users WHERE id = ?", self.id))[0][0]

    async def _update(self, field: str, value: Any) -> None:
        await database.fetch(f"UPDATE users SET {field} = ? WHERE id = ?", value, self.id)
    
    @property
    async def is_admin(self) -> bool:
        return bool(await self._query("is_admin"))
    async def set_admin(self, value: bool) -> None:
        await self._update("is_admin", int(value))
    
    @property
    async def is_manager(self) -> bool:
        return bool(await self._query("is_manager"))
    async def set_manager(self, value: bool) -> None:
        await self._update("is_manager", int(value))

    @property
    async def notification(self) -> bool:
        return bool(await self._query("notification"))
    async def set_notification(self, value: bool) -> None:
        await self._update("notification", int(value))
        
    @property
    async def date_created(self) -> datetime.datetime:
        return datetime.datetime.strptime(await self._query("date_created"), constants.TIME_FORMAT)

    @property
    def cart(self) -> "Cart":
        return self.__Cart(self)
    
    class __Cart:
        def __init__(self, user: "User") -> None:
            self.__user = user

        async def _get_data(self) -> dict:
            return json.loads(await self.__user._query("cart"))
        
        async def _set_data(self, data: dict) -> None:
            await self.__user._update("cart", json.dumps(data))

        @property
        def items(self) -> "__Items":
            return (self.__Items(self))

        class __Items:
            def __init__(self, cart: "__Cart") -> None:
                self.__cart = cart
            
            @property
            async def dict(self) -> dict:
                return (await self.__cart._get_data())["items"]

            async def add(self, item_id: int) -> None:
                data = await self.dict

                if item_id in data:
                    data[item_id] += 1
                else:
                    data[item_id] = 1

                await self.__cart._set_data(data)
            
            async def remove(self, item_id: int) -> None:
                data = await self.dict

                if item_id in data:
                    data[item_id] -= 1
                else:
                    return

                await self.__cart.__set_data(data)
            
            async def clear(self) -> None:
                await self.__cart.__set_data({})

            async def get_quantity(self, item_id: int) -> int:
                return await self.__get_data()[item_id]

        @property
        async def delivery(self) -> int:
            return await self.__get_data()["delivery"]
        async def set_delivery(self, delivery_id: int) -> None:
            data = await self.__get_data()
            data["delivery"] = delivery_id
            await self.__set_data(data)

        @property
        async def payment(self) -> int:
            return await self.__get_data()["payment"]
        async def set_payment(self, payment_id: int) -> None:
            data = await self.__get_data()
            data["payment"] = payment_id
            await self.__set_data(data)

