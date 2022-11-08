import requests
import chardet


## function that gets the random quote
def generate_quote():
    try:
        ## making the get request
        response = requests.get("https://quote-garden.herokuapp.com/api/v3/quotes/random")
        if response.status_code == 200:
            ## extracting the core data
            json_data = response.json()
            data = json_data['data']

            ## getting the quote from the data
            quote = data[0]['quoteText'] 
            author = data[0]['quoteAuthor'] 
            print(f"We want to remind you: {quote} ({author})") 

        else:
            print("Error while getting quote")
    except:
        print("Something went wrong! Try Again!")


def csv_read_and_break_filter(datafile):
    """
    Reads in a csv file and filters any metadata separated from main data by a line break.
    :param datafile: Location of csv file, or pre-opened file.
    :return: List of filtered datapoints.
    """

    if isinstance(datafile, str):
        encoding = chardet.detect(open(datafile, 'rb').read())['encoding']  # just in case file is not standard utf-8
        with open(datafile, "r", encoding=encoding) as f:
            lines = f.readlines()
    else:
        lines = datafile.readlines()
        try:
            lines = [line.decode('utf-8').replace('\r', '') for line in lines]
        except:  # this is a quick patch for one case, TODO: find a way to decipher encoding directly from file
            lines = [line.decode('ISO-8859-1').replace('\r', '') for line in lines]

    unfiltered_lines = [sub.split(",") for sub in lines]

    data_end = 0
    for l_index, line in enumerate(unfiltered_lines):
        # logs are separated from data by a single blank line - this will detect and remove all logs after this line
        if line == ['\n']:
            data_end = l_index
            break

    return unfiltered_lines[0:data_end]

