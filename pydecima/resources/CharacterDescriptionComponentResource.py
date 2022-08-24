from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.LocalizedTextResource import LocalizedTextResource
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string

# TODO: Unfinished


class CharacterDescriptionComponentResource(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        self.character_name: Ref[LocalizedTextResource] = Ref(stream, self.version)
        self.unk_1 = Ref(stream, self.version)
        assert self.unk_1.type == 0
        self.character_type_class = Ref(stream, self.version)
        self.unk_2 = Ref(stream, self.version)
        assert self.unk_2.type == 0

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
