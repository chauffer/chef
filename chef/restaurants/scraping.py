import requests
import re
import unicodedata
import contextlib


class Scraping:

    def get_content(self) -> str:
        r = requests.get(
            self.url,
            timeout=5,
        )
        r.raise_for_status()

        with contextlib.suppress(AttributeError):
            r.encoding = self.encoding
        return r.text

    def get(self):
        matches = []

        content = self.get_content()
        for match in re.findall(self.regex, content, re.MULTILINE):

            with contextlib.suppress(AttributeError):
                if any(blacklist in match for blacklist in self.blacklist):
                    continue

            matches.append(unicodedata.normalize('NFKD', match).strip())
        return matches
