def handle_list_of_tuples(tuples_list):
    """The function that takes list of tuples and sort it
    based on the 'name/age/height/weight' rule.
    Also we need to sort height in reverse order.
    :param tuples_list: list of tuples
    :return: sorted list of tuples by required rule
    """
    return sorted(tuples_list, key=lambda item: (
        item[0],
        item[1],
        -int(item[2]),  # Here, our goal is to reverse sort by height
        item[3]
    ))


def main():
    items_list = [
        ("Tom", "19", "167", "54"),
        ("Jony", "24", "180", "69"),
        ("Json", "21", "185", "75"),
        ("John", "27", "190", "87"),
        ("Jony", "24", "191", "98"),
    ]
    print(handle_list_of_tuples(items_list))


if __name__ == '__main__':
    main()
