from abc import ABC, abstractmethod

from src.libs.business_rules.schemas import (
    UserCoordinates,
    UserLocation,
    UserName,
    UserPicture,
    UserTimezone,
    UserMetadata,
)


class BusinessRulesInterface(ABC):
    @abstractmethod
    def run(self) -> UserMetadata | None: ...

    @abstractmethod
    def create_user_name(self) -> UserName | None: ...

    @abstractmethod
    def create_user_coordinates(self) -> UserCoordinates | None: ...

    @abstractmethod
    def create_user_timezone(self) -> UserTimezone | None: ...

    @abstractmethod
    def create_user_location(self) -> UserLocation | None: ...

    @abstractmethod
    def create_user_picture(self) -> UserPicture | None: ...

    @abstractmethod
    def create_user_metadata(
        self,
        name: UserName,
        location: UserLocation,
        picture: UserPicture,
    ) -> UserMetadata | None: ...
