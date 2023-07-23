from abc import ABC, abstractmethod
from typing import Protocol, TYPE_CHECKING
from itertools import islice

# Есть много вариантов какой интсрумент использовать.
# Я выбрал instaloader потому что у него много звезд, хорошая гибкость, поддержка и свежие обновления.
# Однако, для 1-ой единственной такой задачи он может быть слишком громоздким.
import instaloader

if TYPE_CHECKING:
    pass


class ScrapperProtocol(Protocol, ):
    """self attrs description"""
    L: instaloader.Instaloader


class ScrapperInterface(ABC, ):

    def __init__(self, ): pass

    @abstractmethod
    def get_photos(self, username: str, max_count: int, ) -> list[str]: pass


class Scrapper:

    def __init__(self, *args, **kwargs, ):
        self.L = instaloader.Instaloader(*args, **kwargs, )

    async def get_photos(self, username: str, max_count: int, ) -> list[str]:
        profile = instaloader.Profile.from_username(context=self.L.context, username=username, )
        urls = []  # list comprehension faster but regular list easiest to debug
        # Unfortunately no pagination for this method, maybe instagram itself not support it.
        for post in islice(profile.get_posts(), max_count, ):  # Using islice is more efficient for large iterables
            urls.append(post.url)
        return urls


scrapper = Scrapper()
