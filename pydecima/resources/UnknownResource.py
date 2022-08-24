from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.Resource import Resource


class UnknownResource(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        start_pos = stream.tell()
        Resource.__init__(self, stream, version)
        if self.uuid[:2] == b'\x00\x00':
            print('{} likely has starting short'.format(self.type))
            stream.seek(start_pos + 14)
            self.uuid = stream.read(16)
        stream.seek(start_pos)
        self.data = stream.read(self.size + 12)
