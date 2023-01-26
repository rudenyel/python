import os
import sys


class Accumulator:
    def __init__(self, value=None):
        self._value = None
        if value is not None:
            self._value = self.__verify_value(value)

    @classmethod
    def __verify_value(cls, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            raise ValueError(f'Value "{value}" cannot be converted to int.')

    @property
    def value(self):
        return self._value

    def calc(self, value):
        if self._value is None:
            self._value = self.__verify_value(value)
        else:
            try:
                self._value = self._exec(self.__verify_value(value))
            except ZeroDivisionError:
                raise ValueError('Can''t divide by zero.')
            except OverflowError:
                raise ValueError(f'Function ({self._value}, {value})'
                                 f'causes to overflow.')
        return self._value

    def _exec(self, value):
        raise NotImplementedError


class Summer(Accumulator):
    def _exec(self, value):
        return self._value + value


class Subtractor(Accumulator):
    def _exec(self, value):
        return self._value - value


class Multiplier(Accumulator):
    def _exec(self, value):
        return self._value * value


class Divider(Accumulator):
    def _exec(self, value):
        return self._value // value


def get_func(operation):
    try:
        return {
            'add': Summer,
            'sub': Subtractor,
            'mul': Multiplier,
            'div': Divider,
        }[operation]()
    except KeyError:
        print(f'FUNCTION "{operation}" is unknown.')
        print('Default FUNCTION "add".')
        return Summer()


if __name__ == '__main__':
    method_name = 'add'
    try:
        method_name = os.environ['FUNCTION']
        print(f'The environment variable FUNCTION is {method_name}')
    except KeyError:
        print('The environment variable FUNCTION is missing.')
        print('Default FUNCTION "add".')

    func = get_func(method_name)
    try:
        if len(sys.argv) > 1:
            for operand in sys.argv[1:len(sys.argv)]:
                func.calc(operand)
        print(f'Result is {func.value}')
    except ValueError as error:
        print(error)
        sys.exit(2)
