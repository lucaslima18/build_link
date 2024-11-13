from dataclasses import dataclass
from typing import List


@dataclass
class UserName:
    title: str
    first: str
    last: str


@dataclass
class UserCoordinates:
    latitude: str
    longitude: str


@dataclass
class UserTimezone:
    offset: str
    description: str


@dataclass
class UserLocation:
    street: str
    city: str
    state: str
    postcode: str
    coordinates: UserCoordinates
    timezone: UserTimezone


@dataclass
class UserPicture:
    large: str
    medium: str
    thumbnail: str


@dataclass
class UserMetadata:
    user_type: str  # TODO: come to enum
    gender: str  # TODO come to enum too
    name: UserName
    location: UserLocation
    email: str
    birthday: str
    registered: str
    telephone_numbers: List[str]  # TODO remember conversion on E.164
    mobile_numbers: List[str]
    picture: UserPicture
    nationality: str = "BR"
