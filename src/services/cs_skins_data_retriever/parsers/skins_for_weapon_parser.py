from typing import List

from bs4 import BeautifulSoup


class SkinsForWeaponParser:
    @staticmethod
    def parse(response: str):
        soup = BeautifulSoup(response, 'lxml')
        skin_box_headers = soup.find_all('div', class_='skin-box-header')
        return SkinsForWeaponParser._find_skin_name(skin_box_headers)

    @staticmethod
    def _find_skin_name(skin_box_headers: List[BeautifulSoup]):
        result = []
        for header in skin_box_headers:
            weapon, part, skin = header.text.partition('|')
            result.append(skin.strip())
        return result
