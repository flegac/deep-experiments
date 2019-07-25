import json
import time

from mini_lib.lib1 import func1


def main():
    with open('config.json') as _:
        config = json.load(_)

    func1(config)

    time.sleep(1)
    print('done !')


if __name__ == "__main__":
    main()
