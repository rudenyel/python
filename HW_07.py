import json


class JsonParser:
    def __init__(self, json_str):
        print("environment initialization... done")
        assert isinstance(json_str, str)
        self.json_str = json_str

    def __enter__(self):
        print("context opening... done")
        return json.loads(self.json_str)

    def __exit__(self, ex_type, ex_value, ex_traceback):
        print(f"exception {ex_type}, context closure... done")
        return True


class Point:
    def __init__(self, x, y):
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


class Rectangle:
    def __init__(self, begin, end):
        assert isinstance(begin, Point)
        assert isinstance(end, Point)
        self.upper_left = Point(min(begin.x, end.x), max(begin.y, end.y))
        self.bottom_right = Point(max(begin.x, end.x), min(begin.y, end.y))

    def __str__(self):
        return f"({self.upper_left.x}, {self.upper_left.y}) - " \
               f"({self.bottom_right.x}, {self.bottom_right.y})"

    def contains(self, coordinate):
        assert isinstance(coordinate, Point)
        return (self.upper_left.x <= coordinate.x <= self.bottom_right.x
                and self.bottom_right.y <= coordinate.y <= self.upper_left.y)


if __name__ == '__main__':
    with JsonParser('"hello"') as res:
        print("run operation")
        assert res == "hello"

    with JsonParser('{"hello": "world", "key": [1,2,3]}') as res:
        print("run a divide-by-zero operation")
        assert res == {"hello": "world", "key": [1, 2, 3]}
        raise ZeroDivisionError

    start_point = Point(1, 0)
    print(start_point)
    end_point = Point(-7, 3)
    print(end_point)

    rect = Rectangle(start_point, end_point)
    print(rect)
    # print(start_point)
    # print(end_point)

    assert rect.contains(start_point)
    assert not rect.contains(Point(-1, 4))
