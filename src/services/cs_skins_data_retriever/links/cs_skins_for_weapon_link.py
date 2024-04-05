from src.misc.link_tools import LinkBuilder


class CsSkinsForWeaponkLink:
    @staticmethod
    def create(weapon: str):
        return (
            LinkBuilder('https://www.csgodatabase.com/')
            .add_part_link('weapons/')
            .add_part_link(weapon.lower().replace(' ', '-')).build()
        )