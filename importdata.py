from urllib.request import urlopen
import py7zr
 
from config import *


def download():
    #url = "https://analyticsengineeringprojects.s3.eu-west-1.amazonaws.com/AE_ChessAnalytics.7z"
    #save_as = "AE_ChessAnalytics.7z"
    print(f"Downloading {url}")
    # Download from URL
    with urlopen(url) as file:
        content = file.read()

    # Save to file
    print(f"saving {save_as}")
    with open(f"./data/{save_as}", 'wb') as download:
        download.write(content)

def extract():
    with py7zr.SevenZipFile(f"./data/{save_as}", 'r') as archive:
        archive.extractall(path="./data/")

if __name__=='__main__':
    print(" starting")
    download()
    print(" done ")
    print("extract data")
    extract()
    print("end extraction")
