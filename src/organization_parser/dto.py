from dataclasses import dataclass


@dataclass(frozen=True)
class Company:
    name: str
    address: str
    url: str | None = None

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.address == other.address
            and self.url == other.url
        )
