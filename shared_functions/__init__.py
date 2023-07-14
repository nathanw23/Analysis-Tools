import random
import chardet
from rich import print

## function that gets the random quote
def generate_quote():
    quotes = {
        '"We cannot solve problems with the kind of thinking we employed when we came up with them."': "Albert Einstein",
        '"Learn as if you will live forever, live like you will die tomorrow."': "Mahatma Gandhi",
        '"Power is not given to you"': "Beyonce",
        '"You will face many defeats in life, but never let yourself be defeated"': "Maya Angelou",
        '"It is often the small steps, not the giant leaps, that bring about the most lasting change"': "HM Queen Elizabeth II",
        '"We will fail when we fail to try"': "Rosa Parks",
        '"A person who never made a mistake never tried anything new"': "Albert Einstein",
        '"There is nothing impossible to they who will try"': "Alexander the Great",
        '"Remember that the airplane takes off against the wind, not with it"': "Henry Ford",
        '"Shoot for the moon. Even if you miss, you`ll land among the stars"': "Norman Vincent Peale",
        '"If my mind can conceive it, if my heart can believe it, then I can achieve it"': "Muhammad Ali",
        '"The only way to do great work is to love what you do"': "Steve Jobs",
        '"The best way to predict the future is to create it"': "Abraham Lincoln",
        '"The only person you are destined to become is the person you decide to be"': "Ralph Waldo Emerson",
        '"The best time to plant a tree was 20 years ago. The second best time is now"': "Chinese Proverb",
        '"The best revenge is massive success"': "Frank Sinatra",
        '"Please be patient"': "oxView",
        '"Devise your own paths"': "Vera Rubin",
    }

    quote, author = random.choice(list(quotes.items()))

    print(f"[bold magenta]We want to remind you:[/bold magenta] {quote} ({author})")


def csv_read_and_break_filter(datafile):
    """
    Reads in a csv file and filters any metadata separated from main data by a line break.
    :param datafile: Location of csv file, or pre-opened file.
    :return: List of filtered datapoints.
    """

    if isinstance(datafile, str):
        encoding = chardet.detect(open(datafile, "rb").read())[
            "encoding"
        ]  # just in case file is not standard utf-8
        with open(datafile, "r", encoding=encoding) as f:
            lines = f.readlines()
    else:
        lines = datafile.readlines()
        try:
            lines = [line.decode("utf-8").replace("\r", "") for line in lines]
        except:  # this is a quick patch for one case, TODO: find a way to decipher encoding directly from file
            lines = [line.decode("ISO-8859-1").replace("\r", "") for line in lines]

    unfiltered_lines = [sub.split(",") for sub in lines]

    data_end = 0
    for l_index, line in enumerate(unfiltered_lines):
        # logs are separated from data by a single blank line - this will detect and remove all logs after this line
        if line == ["\n"]:
            data_end = l_index
            break

    return unfiltered_lines[0:data_end]
