from typing import List
import json


class ContactContract(object):

    def __init__(self, name:str, email:str = '', knows=None, belongs=None,
                 tags=None, loves: str = '', hates: str = '') -> None:
        if tags is None:
            tags = []
        if belongs is None:
            belongs = []
        if knows is None:
            knows = []
        self.name = name
        self.knows = knows
        self.belongs = belongs
        self.tags = tags
        self.loves = loves
        self.hates = hates
        self.email = email


    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        return {
            "name": self.name,
            "email": self.email,
            "belongs": self.belongs,
            "knows": self.knows,
            "loves": self.loves,
            "hates": self.hates
        }

class CommunityContract(object):

    def __init__(self, name: str, description: str, owners = None) -> None:
        self.name =  name
        self.description = description
        self.owners = owners

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "owners": self.owners,
        }


class CollectionContract(object):

    def __init__(self, name: str, description: str, owners = None) -> None:
        self.name =  name
        self.description = description
        self.owners = owners

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "owners": self.owners,
        }


