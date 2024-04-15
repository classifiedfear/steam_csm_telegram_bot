from typing import List

from bs4 import BeautifulSoup


class SkinsForWeaponParser:
    @staticmethod
    def parse(response: str):
        soup = BeautifulSoup(response, 'lxml')
        skin_box_headers = soup.find_all('h3', class_='item-box-header')
        return SkinsForWeaponParser._find_skin_name(skin_box_headers)

    @staticmethod
    def _find_skin_name(skin_box_headers: List[BeautifulSoup]):
        result = []
        for item in skin_box_headers:
            result.append(item.text.strip())
        return result
