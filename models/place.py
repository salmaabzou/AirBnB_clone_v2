#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")

place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id", String(60),
        ForeignKey("places.id"),
        primary_key=True, nullable=False,
    ),
    Column(
        "amenity_id", String(60),
        ForeignKey("amenities.id"),
        primary_key=True, nullable=False,
    ),
)


class Place(BaseModel, Base):
    """A place to stay"""

    __tablename__ = "places"
    if storage_type == "db":
        city_id = Column(String(60),
                         ForeignKey("cities.id"),
                         nullable=False)
        user_id = Column(String(60), 
                         ForeignKey("users.id"),
                         nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer,
                              nullable=False, default=0)
        number_bathrooms = Column(Integer,
                                  nullable=False, default=0)
        max_guest = Column(Integer,
                           nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenities = relationship("Amenity",
                                 secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
        reviews = relationship('Review', cascade="all,delete",
                               backref="place")

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def amenities(self):
            """Getter doc"""
            from models import storage
            lsAmen = []
            lsAmenAL = storage.all(Amenity)
            for amenity in lsAmenAL.values():
                if amenity.id in self.amenity_ids:
                    lsAmen.append(amenity)
            return lsAmen

        @property
        def reviews(self):
            """Getter doc"""
            from models import storage
            lsREv = []
            lsREvAl = storage.all(Review)
            for review in lsREvAl.values():
                if review.place_id in self.id:
                    lsREv.append(review)
            return lsREv

        @amenities.setter
        def amenities(self, amenity):
            """Setter doc"""
            if isinstance(amenity, Amenity):
                self.amenity_ids.append(amenity.id)