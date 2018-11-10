def handle_string(value):
    """The function that takes string and return number of digits and letters
    :param value: string
    :return: string with counted Letters and Digits
    """
    digits_count = letters_count = 0
    for char in value:
        if char.isdigit(): digits_count += 1
        elif char.isalpha(): letters_count += 1
    return f"Letters - {letters_count}\nDigits - {digits_count}"


def main():
    print(handle_string("Hello world! 123!"))


if __name__ == '__main__':
    main()
