from abc import ABC, abstractmethod

from app.schemas.osint import Identifier


class PublicCollector(ABC):
    name: str

    @abstractmethod
    async def collect(self, identifier: Identifier) -> list[dict]:
        """Return only publicly available account/profile artifacts."""


class MockCollector(PublicCollector):
    name = "mock_social"

    async def collect(self, identifier: Identifier) -> list[dict]:
        handle = identifier.value.replace("@", "").replace(" ", "_").lower()
        return [
            {
                "platform": "github",
                "handle": handle,
                "profile_url": f"https://github.com/{handle}",
                "metadata": {"source": "public_profile", "collector": self.name},
            },
            {
                "platform": "reddit",
                "handle": handle,
                "profile_url": f"https://www.reddit.com/user/{handle}",
                "metadata": {"source": "public_profile", "collector": self.name},
            },
        ]
