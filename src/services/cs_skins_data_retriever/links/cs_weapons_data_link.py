from src.misc.link_tools import LinkBuilder


class CsWeaponsDataLink:
    @staticmethod
    def create():
        return (
            LinkBuilder('https://www.csgodatabase.com/')
            .add_part_link('weapons/').build()
        )