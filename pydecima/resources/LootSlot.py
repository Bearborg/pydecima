import struct
from typing import BinaryIO, List
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.LootData import LootData
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string


class LootSlot(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        ref_count = struct.unpack('<I', stream.read(4))[0]
        self.loot_data: List[Ref[LootData]] = [Ref(stream, self.version) for _ in range(ref_count)]
        self.loot_slot_settings: Ref = Ref(stream, self.version)

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
