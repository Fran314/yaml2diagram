import sys
import requests

def url(icon):
    return f'https://raw.githubusercontent.com/google/material-design-icons/refs/heads/master/symbols/web/{icon}/materialsymbolsrounded/{icon}_wght700fill1_40px.svg'

class MaterialIcons:
    cache = {}

    def get(self, icon):

        if icon not in self.cache:
            try:
                response = requests.get(url(icon))
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(e, file=sys.stderr)
                print("", file=sys.stderr)
                print(f'Error occurred when fetching icon "{icon}"', file=sys.stderr)

            self.cache[icon] = response.text

        return self.cache[icon]
