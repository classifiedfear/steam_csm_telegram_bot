import json


class StatTrakParser:
    @staticmethod
    def parse(response: str):
        json_response = json.loads(response)
        get_min_available = json_response['data']['get_min_available']
        print(json_response)
        for item in get_min_available:
            if item['isStatTrack']:
                return True
        return False
