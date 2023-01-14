from urllib.request import urlopen
import py7zr
from config import *

# Download and extract data

def download():
    #url = "https://analyticsengineeringprojects.s3.eu-west-1.amazonaws.com/AE_ChessAnalytics.7z"
    #save_as = "AE_ChessAnalytics.7z"
    print(f"Downloading {url}...                                                        ", end='\r')
    # Download from URL
    with urlopen(url) as file:
        content = file.read()

    # Save to file
    print(f"Saving {save_as} ...                                                                             ", end='\r')
    with open(f"./data/{save_as}", 'wb') as download:
        download.write(content)

def extract():
    print(f"Extracting {save_as} ...                                                                             ", end='\r')
    with py7zr.SevenZipFile(f"./data/{save_as}", 'r') as archive:
        archive.extractall(path="./data/")

