from typing import List, Dict, Any

from src.services.csm.exceptions import RequestException


class CsmMarketSkinAssetIdParser:
    @staticmethod
    def parse(response: Dict[str, Any]) -> List[int]:
        CsmMarketSkinAssetIdParser._check_response(response)
        return CsmMarketSkinAssetIdParser._find_asset_id_list(response)

    @staticmethod
    def _find_asset_id_list(response: Dict[str, Any]) -> List[int]:
        asset_id_list = []
        for item in response['items']:
            if (overpay := item.get('overpay')) and (overpay.get('float')):
                asset_id_list.append(item['assetId'])
        return asset_id_list

    @staticmethod
    def _check_response(response: Dict[str, Any]):
        if response.get('error'):
            raise RequestException('No more data available, or invalid skin info')