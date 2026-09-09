from pydantic import BaseModel, WrapValidator
from typing import Annotated



class Config:
    def __init__(self):
        self.highscore_filename = "highscore.json"
        self.level = [1, 2, 3, 4, 5]
        self.width = [15, 20, 30, 25, 10]
        self.height = [15, 20, 30, 25, 10]
        self.lives = 3
        self.pacgum= 42
        self.points_per_pacgum = 10
        self.points_per_super_pacgum = 50
        self.points_per_ghost = 200
        self.seed = 42