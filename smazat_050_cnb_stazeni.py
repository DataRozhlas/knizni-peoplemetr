# MOMENTÁLNĚ NEFUNKČNÍ POLOTOVAR

import os
import urllib.request
import gzip
import shutil
import argparse

def download_files(url_list, folder, download_new_only):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    for url in url_list:
        print(f"Stahuji {url}.")
        # Extract the filename from the URL
        filename = url.split('/')[-1]
        filepath = os.path.join(folder, filename)

        # Check if the file already exists in the folder
        if download_new_only and os.path.exists(filepath[:-3]):
            print(f"Skipping download: {filename} (already exists)")
            continue

        # Download the file
        try:
            urllib.request.urlretrieve(url, filepath)
            print(f"Downloaded: {filename}")

            # Check if the file is compressed (.gz extension)
            if filename.endswith('.gz'):
                # Decompress the file
                with gzip.open(filepath, 'rb') as f_in:
                    with open(filepath[:-3], 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                print(f"Decompressed: {filename}")

                # Remove the compressed file
                os.remove(filepath)

            # Check if the downloaded file is smaller than the existing file
            if os.path.exists(filepath[:-3]):
                existing_size = os.path.getsize(filepath[:-3])
                downloaded_size = os.path.getsize(filepath[:-3])

                if downloaded_size < existing_size:
                    print(f"Downloaded file is smaller than existing file. Deleting downloaded file.")
                    os.remove(filepath[:-3])

        except Exception as e:
            print(f"Failed to download: {filename}")
            print(f"Error: {str(e)}")

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Download files from URLs")
parser.add_argument("-n", "--new-only", action="store_true", help="Download only new files")
args = parser.parse_args()

url_list = [
    "https://aleph.nkp.cz/data/cnb.xml.gz",
    "https://aleph.nkp.cz/data/aut_fd.xml.gz",
    "https://aleph.nkp.cz/data/aut_ch.xml.gz"
]

folder = "downloads"

download_files(url_list, folder, args.new_only)