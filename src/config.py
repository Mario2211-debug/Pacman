import json
from pydantic import BaseModel, Field, ValidationInfo, model_validator
from pydantic.functional_validators import WrapValidator
from typing import Any, Annotated


CONFIG_DEFAULTS = {
    "highscore_filename": "highscore.json",
    "lives": 3,
    "pacgum": 42,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level": [
        {"width": 10, "height": 10},
        {"width": 10, "height": 10},
        {"width": 10, "height": 10},
        {"width": 10, "height": 10},
        {"width": 10, "height": 10},
        {"width": 10, "height": 10},
        {"width": 10, "height": 10},
        {"width": 10, "height": 10},
        {"width": 10, "height": 10},
        {"width": 10, "height": 10}
        ]
    }

def open_config_file(filename: str) -> Any:
    try:
        with open(filename, "r") as f:
            config_content = "".join(line for line in f.readlines() if not line.lstrip().startswith(('#', '//')))
            return json.loads(config_content)
    except Exception as err:
        print("\033[91mConfig file is invalid.")
        print("Default config loaded.\033[0m")
        return CONFIG_DEFAULTS

def validate_config_fields(value: Any, handler, info: ValidationInfo) -> Any:
    try:
        return handler(value)
    except ValueError:
        if value is None:
            print(f"\033[91mMissed value for \"{info.field_name}\"")
        else:
            print(f"\033[91mInvalid value for \"{info.field_name}\": {value}.")
        print(f"Using default: {CONFIG_DEFAULTS.get(info.field_name)}.\033[0m")
        return CONFIG_DEFAULTS.get(info.field_name)


class Config(BaseModel):
    highscore_filename: Annotated[str,
                                  Field(min_length=1,
                                        default=None,
                                        validate_default=True),
                                  WrapValidator(validate_config_fields)]
    level: Annotated[list[dict[str, int]],
                     Field(min_length=1, default=None, validate_default=True),
                     WrapValidator(validate_config_fields)]
    lives: Annotated[int,
                     Field(ge=1, default=None, validate_default=True),
                     WrapValidator(validate_config_fields)]
    pacgum: Annotated[int,
                      Field(ge=1, default=None, validate_default=True),
                      WrapValidator(validate_config_fields)]
    points_per_pacgum: Annotated[int,
                                 Field(ge=1,
                                       default=None,
                                       validate_default=True),
                                 WrapValidator(validate_config_fields)]
    points_per_super_pacgum: Annotated[int,
                                       Field(ge=1,
                                             default=None,
                                             validate_default=True),
                                       WrapValidator(validate_config_fields)]
    points_per_ghost: Annotated[int,
                                Field(ge=1,
                                      default=None,
                                      validate_default=True),
                                WrapValidator(validate_config_fields)]
    seed: Annotated[int,
                    Field(ge=1, default=None, validate_default=True),
                    WrapValidator(validate_config_fields)]

    @model_validator(mode='after')
    def check_level_list(self) -> "Config":

        if not self.highscore_filename.lower().endswith(".json"):
            print(f'\033[91mInvalid value for "highscore_filename".')
            print(f'Using default: "highscore.json"')
            self.highscore_filename = CONFIG_DEFAULTS.get("highscore_filename")

        i = 0
        while i < len(self.level):
            if (self.level[i].get("width") is None
                and self.level[i].get("height") is None):
                self.level.pop(i)
                continue

            if self.level[i].get("width") is None:
                print(f'\033[91mMissed value "width" for level {i + 1}')
                print(f'Using default: 10.\033[0m')
                self.level[i]["width"] = 10
            elif self.level[i].get("width") < 5:
                print(f'\033[91mValue "width" for level {i + 1} is too small.')
                print(f'Using default: 10.\033[0m')
                self.level[i]["width"] = 10

            if self.level[i].get("height") is None:
                print(f'\033[91mMissed value "height" for level {i + 1}')
                print(f'Using default: 10.\033[0m')
                self.level[i]["height"] = 10
            elif self.level[i].get("height") < 5:
                print(f'\033[91mValue "height" for level {i + 1} is too small.')
                print(f'Using default: 10.\033[0m')
                self.level[i]["height"] = 10

            i += 1

        if len(self.level) < 10:
            print('\033[91mNumber of levels must be at least 10.')
            print(f'{10 - len(self.level)} added.\033[0m')
            for i in range(10 - len(self.level)):
                self.level.append({"width": 10, "height": 10})

        return self
