import json
import time


def main():
    with open('config.json') as _:
        config = json.load(_)

    print('training with params={}'.format(str(config)))
    time.sleep(1)
    print('done !')


if __name__ == "__main__":
    main()
