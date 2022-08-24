import struct
from typing import BinaryIO, List
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.LootItem import LootItem
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string


class LootData(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        self.probability: float = struct.unpack('<f', stream.read(4))[0]
        self.unkRef = Ref(stream, self.version)  # Never seems to be valid(?)
        ref_count = struct.unpack('<I', stream.read(4))[0]
        self.loot_item: List[Ref[LootItem]] = [Ref(stream, self.version) for _ in range(ref_count)]
        self.quantity: int = struct.unpack('<I', stream.read(4))[0]
        self.unk3: int = struct.unpack('<b', stream.read(1))[0]

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
