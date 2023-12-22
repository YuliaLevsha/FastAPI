from datetime import datetime
from pydantic import BaseModel


class Streams(BaseModel):
    stream_name: str
    streamer_name: str
    game_name: str
    viewers: int
    data_instance: datetime

    def __str__(self):
        return (
            "Stream name: "
            + self.stream_name
            + ", "
            + "streamer name: "
            + self.streamer_name
            + ", "
            + ""
            "game name: "
            + self.game_name
            + ", "
            + "viewers: "
            + str(self.viewers)
            + ", "
            + "data: "
            + self.data_instance.strftime("%Y-%m-%d %H:%M")
        )


class Games(BaseModel):
    name: str
    data_instance: datetime

    def __str__(self):
        return (
            "Name: "
            + self.name
            + ", "
            + "data: "
            + self.data_instance.strftime("%Y-%m-%d %H:%M")
        )


class Streamers(BaseModel):
    login: str
    name: str
    data_create: datetime
    data_instance: datetime

    def __str__(self):
        return (
            "Login: "
            + self.login
            + ", "
            + "name: "
            + self.name
            + ", "
            + "data create: "
            + self.data_create.strftime("%Y-%m-%d %H:%M")
            + ", "
            + "data instance: "
            + self.data_instance.strftime("%Y-%m-%d %H:%M")
        )
