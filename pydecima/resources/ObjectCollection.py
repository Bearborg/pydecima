import struct
from typing import BinaryIO, List
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref


class ObjectCollection(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        objects_count = struct.unpack('<I', stream.read(4))[0]
        self.objects: List[Ref] = [Ref(stream, self.version) for _ in range(objects_count)]
