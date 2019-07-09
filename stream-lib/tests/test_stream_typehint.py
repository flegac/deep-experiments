from stream_lib.stream import stream

int_sequence = list(range(10))


def to_string(x: float) -> str:
    return str(x)


def treshold(x: float) -> bool:
    return x > 3.0


def test_map():
    result = stream(int_sequence) \
        .map(float) \
        .filter(treshold) \
        .map(to_string) \
        .to_list()
    print(result)


def test_enumerate():
    result = stream(int_sequence) \
        .map(to_string) \
        .enumerate() \
        .to_list()
    print(result)
