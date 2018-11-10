def handle_numbers(number1, number2, number3):
    """The function that count numbers of integers that divisible by number 3
    :param number1: integer number
    :param number2: integer number
    :param number3: integer number
    :return: return the count of integers that are divisible
    by number3 in range [number1, number2]
    """
    if number1 % number3 == 0:
        return ((number2 // number3) - (number1 // number3)) + 1
    return (number2 // number3) - (number1 // number3)


def main():
    print(handle_numbers(1, 10, 2))


if __name__ == '__main__':
    main()
