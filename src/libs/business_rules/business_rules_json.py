from csv import register_dialect
from typing import Dict

from src.shared.utils.convert_phone import convert_phone
from src.shared.utils.convert_gender import convert_gender
from src.shared.utils.convert_user_type import convert_user_type
from src.libs.business_rules.ext import InvalidGenderException
from src.libs.business_rules.interfaces import BusinessRulesInterface
from src.libs.business_rules.schemas import (
    UserCoordinates,
    UserLocation,
    UserMetadata,
    UserName,
    UserPicture,
    UserTimezone,
)
from src.shared.utils.log_handler import LogHandler

logger = LogHandler()


class BusinessRulesJSON(BusinessRulesInterface):
    def __init__(self, data: Dict, content_type: str) -> None:
        self.data = data
        self.content_type = content_type

    def run(self) -> UserMetadata | None:
        name = self.create_user_name()
        location = self.create_user_location()
        picture = self.create_user_picture()

        return self.create_user_metadata(
            name=name,
            location=location,
            picture=picture,
        )

    def create_user_name(self) -> UserName:
        user_name = UserName(
            title=self.data["name"]["title"],
            first=self.data["name"]["first"],
            last=self.data["name"]["last"],
        )

        return user_name

    def create_user_coordinates(self) -> UserCoordinates:
        user_coordinates = UserCoordinates(
            latitude=self.data["location"]["coordinates"]["latitude"],
            longitude=self.data["location"]["coordinates"]["longitude"],
        )

        return user_coordinates

    def create_user_timezone(self) -> UserTimezone:
        user_timezone = UserTimezone(
            offset=self.data["location"]["timezone"]["offset"],
            description=self.data["location"]["timezone"]["description"],
        )

        return user_timezone

    def create_user_location(self) -> UserLocation:
        user_location = UserLocation(
            street=self.data["location"]["street"],
            city=self.data["location"]["city"],
            state=self.data["location"]["state"],
            postcode=str(self.data["location"]["postcode"]),
            coordinates=self.create_user_coordinates(),
            timezone=self.create_user_timezone(),
        )

        return user_location

    def create_user_picture(self) -> UserPicture:
        user_picture = UserPicture(
            large=self.data["picture"]["large"],
            medium=self.data["picture"]["medium"],
            thumbnail=self.data["picture"]["thumbnail"],
        )

        return user_picture

    def create_user_metadata(
        self,
        name: UserName,
        location: UserLocation,
        picture: UserPicture,
    ) -> UserMetadata | None:
        try:
            nationality = self.data.get("nationality", "BR")
            user_metadata = UserMetadata(
                user_type=convert_user_type(
                    lat=float(location.coordinates.latitude),
                    lon=float(location.coordinates.longitude),
                ),
                gender=convert_gender(gender=self.data["gender"]),
                name=name,
                location=location,
                email=self.data["email"],
                birthday=self.data["dob"]["date"],
                registered=self.data["registered"]["date"],
                telephone_numbers=[
                    convert_phone(
                        phone_number=self.data["phone"], nationality=nationality
                    )
                ],
                mobile_numbers=[self.data["cell"]],
                picture=picture,
                nationality=nationality,
            )

            return user_metadata

        except Exception as err:
            logger.error(err)
