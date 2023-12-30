import csv
import os
from urllib import request, error
from urllib.parse import urlparse
from PIL import Image
from tqdm import tqdm

# Path to the CSV file
csv_file = '/localdisk0/GDELT/2019-vgkg-protest-image-dataset-20191030-labels.csv'

# Directory to save the images
output_dir = '/localdisk0/GDELT/data/'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Function to download an image from a URL
def download_image(id,index, img_url, output_dir):
    try:
        # Open the URL and read the content
        with request.urlopen(img_url, timeout=5) as response:
            if response.getcode() == 200:

                parsed_url = urlparse(img_url)
                filename = os.path.join(output_dir, f"{str(index)}_{str(id)}{os.path.splitext(parsed_url.path)[1]}")
                # Save the image to the output directory
                with open(filename, 'wb') as f:
                    f.write(response.read())
                if not is_valid_image(filename):
                        print(f"Corrupted image: {img_url}")
                        os.remove(filename)  # Delete the corrupted file
                        return False
                print(f"Downloaded: {img_url}")
                return True
            else:
                print(f"Failed to download: {img_url} - Status code: {response.getcode()}")
    except error.HTTPError as e:
        print(f"Failed to download: {img_url} - HTTPError: {e}")
    except error.URLError as e:
        print(f"Failed to download: {img_url} - URLError: {e}")
    except Exception as e:
        print(f"Failed to download: {img_url} - Error: {e}")

    return False

def is_valid_image(file_path):
    try:
        # Attempt to open the file as an image
        with Image.open(file_path) as img:
            img.verify()  # Verify the integrity of the image file
        return True
    except Exception:
        return False
    
with open(csv_file, 'r', newline='', encoding='utf-8') as file:
    total_rows = sum(1 for _ in file)

# Open the CSV file and iterate over its rows
with open(csv_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=',')
    index = 0
    row_id = 0
    for row in tqdm(reader, total=total_rows):
        #print(row)
        # Get the image URL from the row
        img_url = row[1]
        #print(img_url)
        
        # Download the image
        if download_image(row_id, index, img_url, output_dir):
            index+=1
        row_id+=1

