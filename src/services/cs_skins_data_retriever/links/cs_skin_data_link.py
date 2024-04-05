from src.misc.link_tools import LinkBuilder


class CsSkinDataLink:
    @staticmethod
    def create():
        return (
            LinkBuilder('https://wiki.cs.money/api/graphql')
            .build()
        )