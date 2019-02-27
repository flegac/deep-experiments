from stream_lib.stream import stream, Stream

# ----- DATA --------------------------------------------------
sequence = list(range(5))


def int_transformer(x: int) -> int:
    return x + 3


def stream_transformer(_: Stream[int]):
    return [4, 2]


# ----- TESTS -------------------------------------------------

def test_map():
    actual = stream(sequence) \
        .map(int_transformer) \
        .to_list()

    assert actual == list(map(int_transformer, sequence)), str(actual)


def test_apply():
    actual = stream(sequence) \
        .apply(stream_transformer) \
        .to_list()

    assert actual == list(stream_transformer(stream(sequence))), str(actual)


def test_flatmap():
    actual = stream(sequence) \
        .flatmap(lambda x: stream(range(x + 1))) \
        .to_list()

    assert actual == [0, 0, 1, 0, 1, 2, 0, 1, 2, 3, 0, 1, 2, 3, 4], str(actual)


def test_filter():
    actual = stream(sequence) \
        .filter(lambda x: x % 2 == 0).to_list()

    assert actual == [0, 2, 4], str(actual)


def test_slice():
    actual = stream(sequence) \
        .slice(start=2, stop=7, step=2) \
        .to_list()

    assert actual == [2, 4], str(actual)


def test_limit():
    actual = stream(sequence) \
        .limit(4) \
        .to_list()

    assert actual == [0, 1, 2, 3], str(actual)


def test_flatten():
    actual = stream(sequence) \
        .map(lambda x: stream(range(x + 1))) \
        .flatten() \
        .to_list()

    assert actual == [0, 0, 1, 0, 1, 2, 0, 1, 2, 3, 0, 1, 2, 3, 4], str(actual)


def test_enumerate():
    actual = stream(sequence) \
        .enumerate() \
        .slice(1, 3) \
        .enumerate() \
        .to_list()

    assert actual == [(0, (1, 1)), (1, (2, 2))], str(actual)


def test_side_effect():
    data = []

    def get_data(x):
        data.append(x)

    actual = stream(sequence) \
        .side_effect(get_data) \
        .to_list()

    assert actual == sequence
    assert data == sequence


test_apply()
test_map()
test_flatmap()
test_filter()
test_slice()
test_limit()
test_flatten()
test_enumerate()
test_side_effect()
