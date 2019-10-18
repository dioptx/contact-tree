from typing import List
import json


class ContactContract(object):

    def __init__(self,cid: str, name:str, knows: List[str], belongs: List[str],
                 tags: List[str], loves: str, hates: str, email:str ) -> None:
        self.cid = cid
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

class CommunityContract(object):

    def __init__(self, cid: str) -> None:
        pass

    @classmethod
    def from_json(cls, data):
        return cls(**data)
