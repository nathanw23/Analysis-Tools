from quote import quote
import random
import chardet


def generate_quote(words=("science", "music", "engineering")):
    """
    Generates a fun quote at the end of each run.
    :param words: Keywords to use to generate quote.
    :return: None
    """
    choice = random.choice(words)
    res = quote(choice, limit=100)
    random_number = random.randint(1, 100)
    print(f"We want to remind you: {res[random_number]['quote']} ({res[random_number]['author']})")


def csv_read_and_break_filter(datafile):
    """
    Reads in a csv file and filters any metadata separated from main data by a line break.
    :param datafile: Location of csv file, or pre-opened file.
    :return: List of filtered datapoints.
    """

    encoding = chardet.detect(open(datafile, 'rb').read())['encoding']  # just in case file is not standard utf-8
    if isinstance(datafile, str):
        with open(datafile, "r", encoding=encoding) as f:
            lines = f.readlines()
    else:
        lines = datafile.readlines()
        lines = [line.decode(encoding).replace('\r', '') for line in lines]

    unfiltered_lines = [sub.split(",") for sub in lines]

    data_end = 0
    for l_index, line in enumerate(unfiltered_lines):
        # logs are separated from data by a single blank line - this will detect and remove all logs after this line
        if line == ['\n']:
            data_end = l_index
            break

    return unfiltered_lines[0:data_end]

