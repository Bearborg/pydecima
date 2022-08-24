from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.Resource import Resource


class OutOfBoundsNavMeshArea(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        start_pos = stream.tell()
        Resource.__init__(self, stream, version)
        stream.seek(start_pos + 12)
        stream.read(60)  # TODO: don't skip this
        self.uuid = stream.read(16)
        stream.seek(start_pos)
        self.data = stream.read(self.size + 12)
