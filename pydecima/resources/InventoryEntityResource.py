import struct
from typing import BinaryIO, List
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string


class InventoryEntityResource(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        start_pos = stream.tell()
        Resource.__init__(self, stream, version)
        stream.seek(start_pos + 12)
        self.unk = struct.unpack('<h', stream.read(2))[0]
        self.uuid = stream.read(16)
        self.name = parse_hashed_string(stream)
        stream.read(7)  # TODO
        Ref(stream, self.version)
        stream.read(16)
        self.multiAction = Ref(stream, self.version)
        self.unk3 = Ref(stream, self.version)
        ref_count = struct.unpack('<I', stream.read(4))[0]
        self.ref_list: List[Ref] = [Ref(stream, self.version) for _ in range(ref_count)]

        stream.seek(start_pos)
        self.data = stream.read(self.size + 12)
