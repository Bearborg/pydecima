import struct
from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.Resource import Resource
from pydecima._utils import parse_hashed_string


class InventoryAmmoEjectorResource(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        start_pos = stream.tell()
        Resource.__init__(self, stream, version)
        stream.seek(start_pos + 12)
        self.unk = struct.unpack('<h', stream.read(2))[0]
        self.uuid = stream.read(16)
        self.name = parse_hashed_string(stream)
        stream.seek(start_pos)
        self.data = stream.read(self.size + 12)
