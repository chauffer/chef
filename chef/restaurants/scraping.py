import requests
import re
import unicodedata
import contextlib

class Scraping:
    def get(self):
        r = requests.get(
            self.url,
            timeout=5,
        )
        r.raise_for_status()

        with contextlib.suppress(AttributeError):
            r.encoding = self.encoding

        matches = []

        for match in re.findall(self.regex, r.text, re.MULTILINE):

            with contextlib.suppress(AttributeError):
                if any(blacklist in match for blacklist in self.blacklist):
                    continue

            matches.append(unicodedata.normalize('NFKD', match).strip())
        return matches
