NUMBERS = {
    ((' ', '_', ' '), ('|', ' ', '|'), ('|', '_', '|')): 0,
    ((' ', ' ', ' '), (' ', ' ', '|'), (' ', ' ', '|')): 1,
    ((' ', '_', ' '), (' ', '_', '|'), ('|', '_', ' ')): 2,
    ((' ', '_', ' '), (' ', '_', '|'), (' ', '_', '|')): 3,
    ((' ', ' ', ' '), ('|', '_', '|'), (' ', ' ', '|')): 4,
    ((' ', '_', ' '), ('|', '_', ' '), (' ', '_', '|')): 5,
    ((' ', '_', ' '), ('|', '_', ' '), ('|', '_', '|')): 6,
    ((' ', '_', ' '), (' ', ' ', '|'), (' ', ' ', '|')): 7,
    ((' ', '_', ' '), ('|', '_', '|'), ('|', '_', '|')): 8,
    ((' ', '_', ' '), ('|', '_', '|'), (' ', '_', '|')): 9,
}


def group_account_data(lines_data):
    """Group raw bank account file lines by account

    :param lines_data: a list of line character lists
    :return: a list of 3x27 characters
    """

    sliced = [lines_data[i::4] for i in range(4)]
    zipped = zip(*sliced)

    return [[line for line in group if line is not None] for group in zipped]


def parse_line(line_data, index):
    """Regularize line data - should always be 27 chars long

    :param line_data: a list of chars
    :param index
    """

    return None if (index + 1) % 4 == 0 else line_data + [' '] * (27 - len(line_data))


def read_file(filename):
    """Open and read the file, stripping newlines"""

    with open(filename, 'r') as accounts_file:
        return [line.rstrip('\n') for line in accounts_file]


def parse_file(filename):
    """Read, parse and group file data by account"""

    return group_account_data([parse_line(list(chars), index) for index, chars in enumerate(read_file(filename))])


def group_number_data(raw_account_data):
    """Group raw account character data by number character data

    :param raw_account_data: a 3x27 character list
    :return: a zipped 3x3 characters tuple iterator
    """

    sliced_lines = [[line[i::3] for i in range(3)] for line in raw_account_data]

    return zip(*[zip(*sliced_line) for sliced_line in sliced_lines])


def identify_account_number(number_data):
    """Map character tuple to a number

    :param number_data: a 3x3 character tuple
    :return: a number (-1 for unrecognized numbers)
    """

    try:
        return NUMBERS[number_data]
    except KeyError:
        return -1


def identify_account_numbers(processed_data):
    return [identify_account_number(number_char) for number_char in processed_data]


def checksum(account):
    """Verify the formal validity of an account number

    :param account: in the form of a list of ints
    """

    return sum(d * n for d, n in zip(range(1, 10), account[::-1]))


def build_account_info(account):
    """Build formatted account info

    :param account: in the form of a list of ints
    """

    recognized = -1 not in account
    valid = recognized and checksum(account) % 11 == 0
    return {'num': ''.join(map(lambda c: str(c) if c != -1 else '?', account)), 'rec': recognized, 'val': valid}


def error_info(account_info):
    """Get error code string (if any) for provided account

    :param account_info
    """

    if not account_info['rec']:
        return ' ILL'
    elif not account_info['val']:
        return ' ERR'
    return ''


def write_account_info(accounts_info):
    """Write report file with formatted info

    :param accounts_info
    """
    
    lines = '\n'.join(['%s%s' % (i['num'], error_info(i)) for i in accounts_info])
    with open('data/bankreport.txt', 'w+') as report_file:
        report_file.write(lines)


def generate_report():
    print('Parsing and processing bank accounts file...')

    raw_accounts_data = parse_file('data/bankaccounts.txt')
    processed_accounts_data = [group_number_data(raw_data) for raw_data in raw_accounts_data]
    identified_accounts_data = [identify_account_numbers(number_data) for number_data in processed_accounts_data]
    accounts_info = [build_account_info(account) for account in identified_accounts_data]
    write_account_info(accounts_info)

    print("All done!")


if __name__ == "__main__":
    generate_report()
