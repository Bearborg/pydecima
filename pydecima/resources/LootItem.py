import struct
from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string


class LootItem(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        start_pos = stream.tell()
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        self.unk: float = struct.unpack('<f', stream.read(4))[0]
        self.unk2 = Ref(stream, self.version)
        self.inventoryEntity = Ref(stream, self.version)

        stream.seek(start_pos)
        self.data = stream.read(self.size + 12)

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
