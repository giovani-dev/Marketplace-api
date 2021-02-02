import re


class ValidateCpf(object):
    def __init__(self, cpf_text, full_validation: bool):
        self.cpf_text = cpf_text
        self.is_valid = True
        self._digits = int()
        if full_validation:
            self.full()

    def __bool__(self):
        return self.is_valid

    def __str__(self):
        return ''.join(str(number) for number in self._digits)

    def length(self):
        if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', self.cpf_text ):
            return False
        return self

    def digits(self):
        try:
            self._digits = [int(digit) for digit in self.cpf_text if digit.isdigit()]
        except TypeError:
            return False
        return self

    def __digit_position(self, position: int):
        sum_of_products = sum(a*b for a, b in zip(self._digits[0:position], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if self._digits[position] != expected_digit:
            return False
        return self

    def first_digit(self):
        return self.__digit_position(position=9)

    def second_digit(self):
        return self.__digit_position(position=10)

    def full(self):
        try:
            self.length().digits().first_digit().second_digit()
        except AttributeError:
            self.is_valid = False
