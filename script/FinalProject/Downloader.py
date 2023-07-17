import requests


class Downloader:
    def __init__(self, url):
        self.url = url

    def download_data(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                return response.content
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while downloading the file: {e}")

    def save_to_file(self, data, filename):
        with open(filename, 'wb') as file:
            file.write(data)
