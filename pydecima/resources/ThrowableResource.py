import struct
from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.Resource import Resource


class ThrowableResource(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        start_pos = stream.tell()
        Resource.__init__(self, stream, version)
        stream.seek(start_pos + 12)
        self.unk = struct.unpack('<h', stream.read(2))[0]
        self.uuid = stream.read(16)
        stream.seek(start_pos)
        self.data = stream.read(self.size + 12)
