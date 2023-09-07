from dataclasses import dataclass


@dataclass(frozen=True)
class Company:
    name: str
    address: str
    url: str | None = None
    email: str | None = None
    phone: str | None = None

    def __eq__(self, other):
        return (
            self.__class__.__name__ == other.__class__.__name__
            and self.name == other.name
            and self.address == other.address
            and self.url == other.url
            and self.email == other.email
            and self.phone == other.phone
        )

    def __repr__(self) -> str:
        return f"{self.name} {self.address} {self.url} {self.email} {self.phone}"

    def to_dict(self) -> dict[str, str | None]:
        return dict(
            name=self.name,
            address=self.address,
            url=self.url,
            email=self.email,
            phone=self.phone,
        )
