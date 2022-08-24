from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion
import struct
from pydecima.resources.Resource import Resource

# TODO: Unfinished


class CollisionTrigger(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        start_pos = stream.tell()
        Resource.__init__(self, stream, version)
        stream.seek(start_pos + 12)
        self.unk = struct.unpack('<I', stream.read(4))[0]
        self.uuid = stream.read(16)
        stream.seek(start_pos)
        self.data = stream.read(self.size + 12)
