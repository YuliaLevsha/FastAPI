from pydantic import BaseModel
from datetime import datetime


class Clothes(BaseModel):
    category: str
    gender: str
    name: str
    brand: str
    price: float
    data_instance: datetime

    def __str__(self):
        return (
            "Category: "
            + self.category
            + ", "
            + "gender: "
            + self.gender
            + ", "
            + "name: "
            + self.name
            + ""
            ", "
            + "brand: "
            + self.brand
            + ", "
            + "price: "
            + str(self.price)
            + ", "
            + "data: "
            + self.data_instance.strftime("%Y-%m-%d %H:%M")
        )
