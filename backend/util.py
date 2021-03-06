import os
import json
from uuid import uuid4


def generate_config(config_name, directory=".", **params):
    if not os.path.exists(directory):
        os.mkdir(directory)
    file_path = "{}/{}_{}.json".format(directory, uuid4().hex, config_name)
    params.update({"db_name": uuid4().hex})
    with open(file_path, "w+") as f:
        json.dump(params, f)
    return file_path
