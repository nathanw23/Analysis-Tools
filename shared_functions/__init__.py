from quote import quote
import random


def generate_quote(words=("science", "music", "engineering")):
    choice = random.choice(words)
    res = quote(choice, limit=100)
    random_number = random.randint(1, 100)
    print(f"We want to remind you: {res[random_number]['quote']} ({res[random_number]['author']})")


def csv_read_and_break_filter(datafile):
    """
    Reads in a csv file and filters any metadata separated from main data by a line break.
    :param datafile: Location of csv file.
    :return: List of filtered datapoints.
    """

    f = open(datafile, "r")
    lines = f.readlines()

    unfiltered_lines = [sub.split(",") for sub in lines]

    data_end = 0
    for l_index, line in enumerate(unfiltered_lines):
        # logs are separated from data by a single blank line - this will detect and remove all logs after this line
        if line == ['\n']:
            data_end = l_index
            break

    return unfiltered_lines[0:data_end]

