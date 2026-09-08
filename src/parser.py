import json
from typing import Any

def read_json_file(content: str) -> Any:
    try:
        with open(filename, "r") as f:
            try:
                return json.load(f)

        # lines: list[str] = [line for line in
                            # map(str.strip, content.splitlines())
                            # if line and line[0] != '#']

                print(json.loads(content))
            except Exception:
                print("\033[1;41mJSON parsing error\033[0m")
                print(f"\033[91m File \"{filename}\" "
                      "has wrong format.\033[0m")
                exit()
    except Exception as err:
        print(f"\033[91m{err}\033[0m")
        exit()


"""
def parse_json(json_obj: str, class_name: type[BaseModel]) -> Any:
    result: list[BaseModel] = []
    for x in json_obj:
        try:
            result.append(class_name.model_validate(x))
        except ValidationError as err:
            print(f"\033[1;41m{class_name.__name__} parsing error\033[0m")
            for error in err.errors():
                if error["type"] == "missing":
                    print(f"\033[91mField \"{error["loc"][0]}\" "
                          "is missing.\033[0m")
                elif error["type"] == "string_too_short":
                    print(f"\033[91mField \"{error["loc"][0]}\" "
                          "can't be empty.\033[0m")
                else:
                    print(f"\033[91m{error["msg"]}\033[0m")
    return result
"""