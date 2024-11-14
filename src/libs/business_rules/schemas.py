from typing import List

from pydantic import BaseModel


class UserName(BaseModel):
    title: str
    first: str
    last: str


class UserCoordinates(BaseModel):
    latitude: str
    longitude: str


class UserTimezone(BaseModel):
    offset: str
    description: str


class UserLocation(BaseModel):
    street: str
    city: str
    state: str
    postcode: str
    coordinates: UserCoordinates
    timezone: UserTimezone


class UserPicture(BaseModel):
    large: str
    medium: str
    thumbnail: str


class UserMetadata(BaseModel):
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
