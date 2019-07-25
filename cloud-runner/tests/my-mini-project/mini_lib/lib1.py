import json
from typing import Dict


def func1(conf: Dict):
    print(json.dumps(conf, indent=4, sort_keys=True))
