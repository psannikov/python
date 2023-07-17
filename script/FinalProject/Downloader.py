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

    def download_file(self, filename):
        mb = 1024 * 1024
        gb = mb * 1024
        chunk_size = 500 * mb
        chunk_count = 0
        with requests.get(self.url, stream=True) as r:
            if r.status_code == 200:
                r.raise_for_status()
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        chunk_count += 1
                        f.write(chunk)
                        print(f'Закачано {chunk_count} блоков размером {chunk_size / mb}Мб. '
                              f'Общий объем закачанных данных {float(chunk_count) * chunk_size / gb}Гб')
        return filename
