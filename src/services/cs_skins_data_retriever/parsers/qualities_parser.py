import json


class QualitiesParser:
    @staticmethod
    def parse(response: str):
        qualities = set()
        json_response = json.loads(response)
        get_min_available = json_response['data']['get_min_available']
        for item in get_min_available:
            name = item['name']
            quality = name.split('(')[-1]
            qualities.add(quality[:-1])
        return list(qualities)
