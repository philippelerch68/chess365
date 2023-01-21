from urllib.request import urlopen
import py7zr

# Download and extract data

def download(url, save_as):
    """Downloads a zip folder containing the project's data from defined url: 
    "https://analyticsengineeringprojects.s3.eu-west-1.amazonaws.com/AE_ChessAnalytics.7z"

    Args:
        url (str): URL where the data for the project is received
        save_as (str): Location and name where the zipped folder is stored
    """
    print(f"Downloading {url}...                                                        ", end='\r')
    with urlopen(url) as file:
        content = file.read()

    print(f"Saving {save_as} ...                                                                             ", end='\r')
    with open(save_as, 'wb') as download:
        download.write(content)

def extract(save_as, data_dir):
    """Unzip the folder and store it in a defined location

    Args:
        save_as (str): Location and name where the zipped folder is stored
        data_dir (str): Location where the unzipped folder is stored
    """
    print(f"Extracting {save_as} ...                                                                             ", end='\r')
    with py7zr.SevenZipFile(save_as, 'r') as archive:
        archive.extractall(path=data_dir)

