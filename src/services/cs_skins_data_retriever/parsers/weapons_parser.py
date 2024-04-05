from bs4 import BeautifulSoup


class WeaponsParser:
    @staticmethod
    def parse(response: str):
        soup = BeautifulSoup(response, 'lxml')
        item_boxes = soup.find_all('h3', class_='item-box-header')
        return WeaponsParser._find(item_boxes)

    @staticmethod
    def _find(item_boxes):
        knife_index = float('inf')
        result = []
        for index, item_box in enumerate(item_boxes):
            if index < knife_index:
                weapon_name = item_box.text.strip()
                if weapon_name == 'Negev':
                    knife_index = index + 1
                result.append(item_box.text.strip())
            else:
                result.append(f'★ {item_box.text.strip()}')
        return result
