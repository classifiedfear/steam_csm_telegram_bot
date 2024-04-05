from bs4 import BeautifulSoup


class SkinsForKnifeParser:
    @staticmethod
    def parse(response: str):
        soup = BeautifulSoup(response, 'lxml')
        item_boxes = soup.find_all('h3', class_='item-box-header')
        return SkinsForKnifeParser._find(item_boxes)

    @staticmethod
    def _find(item_boxes):
        result = []
        for item in item_boxes[1:]:
            result.append(item.text.strip())
        return result
