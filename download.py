import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import unquote
from zipfile import ZipFile

hack_title = 'super dram world'

def get_hack_url_by_title(hack_title):
    gs = f'https://www.google.com/search?q={hack_title.replace(" ", "+")}&q=site%3Asmwcentral.net&go=Go'
    response = requests.get(gs)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        top_h3 = soup.find('h3')
        top_link = top_h3.find_parent('a')['href']
        encoded_url = top_link.split('=')[1]
        decoded_url = unquote(encoded_url)
        if not decoded_url.startswith('https://www.smwcentral.net/?p=section&a=details&id='):
            raise ValueError("Unexpected URL")
        return decoded_url
    else: print("Failed")

def get_suggested_filename(response):
    content_disposition = response.headers.get('Content-Disposition')
    if content_disposition:
        _, params = content_disposition.split(';', 1)
        for param in params.split(';'):
            key, value = param.strip().split('=')
            if key.lower() == 'filename':
                return unquote(value.strip('\'"'))
    return None

# split logic here. get_hack_name - confirm it - download_hack
def download_hack():
    response = requests.get("https://www.smwcentral.net/?p=section&a=details&id=11374&sa")

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        donwload_btn = soup.find('a', class_="button action")
        donwload_url = f'https:{donwload_btn["href"]}'
        hack_title = soup.find('h1')

    else: print("Failed")

    target_path = os.path.join(os.path.expanduser("~"), 'Desktop')

    try:
        response = requests.get(donwload_url, stream=True)
        response.raise_for_status()

        suggested_filename = get_suggested_filename(response)
        zip_file_name = suggested_filename or 'downloaded_file.zip'
        zip_file_path = os.path.join(target_path, zip_file_name)

        with open(zip_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        print(f"File downloaded successfully to {zip_file_path}")

        with ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(target_path)

        print(f"Files extracted successfully to {target_path}")

        bps_files = [filename for filename in os.listdir(target_path) if filename.lower().endswith('.bps')]
        if bps_files:
            print(f"Found BPS file(s): {bps_files}")
        else:
            print("No BPS files found in the extracted directory")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download file. Error: {e}")
