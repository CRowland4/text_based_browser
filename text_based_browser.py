import os
import sys
import requests
from bs4 import BeautifulSoup
from colorama import Fore, init

init()


class TextBrowser:
    def __init__(self):
        self.cache_directory = ''
        self.url = ''
        self.response = None
        self.html_content = ''
        self.soup = ''
        self.soup_text = ''
        self.file_name = ''
        self.stored_sites = []
        self.stacked_file_names = []
        return

    def launch_browser(self):
        self._create_directory()
        while True:
            self._get_url()

            if self._check_for_back():
                continue

            if self._validate_url():
                pass
            else:
                break

            self._set_html_attribute()
            self._set_file_name()
            self._stack_file_name()
            self._filter_soup()
            self._set_tag_text()
            self._create_url_file()
            self._print_content()

    def _create_directory(self):
        """Creates a directory to store website information. Directory name comes from command line."""
        self.cache_directory = sys.argv[1]
        if os.path.isdir(self.cache_directory):
            return
        else:
            os.mkdir(self.cache_directory)
            return

    def _get_url(self):
        """Gets a url from the user. Responds to the exit command."""
        self.url = input()
        self._check_for_exit()
        return

    def _check_for_exit(self):
        """Exits the program if a user enters 'exit'."""
        if self.url == 'exit':
            sys.exit()
        return

    def _check_for_back(self):
        """Executes the back command if the user has entered 'back'."""
        if self.url == 'back' and len(self.stacked_file_names) > 1:
            del self.stacked_file_names[-1]
            self.file_name = self.stacked_file_names[-1]
            self._print_content()
            return True
        elif self.url == 'back':
            return True

        return False

    def _validate_url(self):
        """Adds 'https://' if it's missing from the user-entered url."""
        if '.' not in self.url:
            print("Incorrect URL")
            return False

        if not self.url.startswith("https"):
            old_url = self.url
            self.url = "https://" + old_url

        return True

    def _set_html_attribute(self):
        """Adds the html content of the requested webpage to the html attribute."""
        self.response = requests.get(self.url)
        self.html_content = self.response.text
        return

    def _set_file_name(self):
        """Creates a file name out of the given url."""
        if '//' in self.url:
            first_slash_index = self.url.index('/')
        else:
            first_slash_index = 0

        if '.' in self.url:
            dot_index = self.url.index('.')
        else:
            dot_index = len(self.url)

        self.file_name = self.url[first_slash_index + 2:dot_index]
        return

    def _stack_file_name(self):
        """Adds the requested url to the url stack."""
        self.stacked_file_names.append(self.file_name)
        return

    def _filter_soup(self):
        """Sets the soup attribute as a list that only contains p, headers, a, ul, ol, and li tags."""
        soup = BeautifulSoup(self.html_content, 'html.parser')
        tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']
        self.soup = soup.find_all(tags)
        return

    def _set_tag_text(self):
        """Gets the filtered soup text, with link text in blue."""
        text = []

        for tag in self.soup:

            if tag.get_text() and tag.name != 'a':
                text.append(tag.get_text())
            elif tag.get_text():
                string = tag.get_text()
                text.append(Fore.BLUE + string)

        self.soup_text = '\n'.join(text)
        return

    def _create_url_file(self):
        """Creates a file with the content of the given url if one doesn't exists already."""
        if os.path.isfile(f'{self.cache_directory}/{self.file_name}'):
            return

        with open(f'{self.cache_directory}/{self.file_name}', 'w', encoding='utf-8') as file:
            file.write(self.soup_text)
        self.stored_sites.append(self.file_name)

        return

    def _print_content(self):
        """Prints the content of the specified url."""
        print(self.soup_text)
        return


my_browser = TextBrowser()
my_browser.launch_browser()


