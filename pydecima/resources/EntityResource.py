import struct
from typing import BinaryIO, List
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string


# TODO: Unfinished


class EntityResource(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        start_pos = stream.tell()
        Resource.__init__(self, stream, version)
        stream.seek(start_pos + 12)
        self.unk1 = struct.unpack('<h', stream.read(2))[0]
        self.uuid = stream.read(16)
        self.name = parse_hashed_string(stream)
        stream.read(6)  # TODO
        Ref(stream, self.version)
        Ref(stream, self.version)
        Ref(stream, self.version)
        stream.read(15)
        Ref(stream, self.version)
        Ref(stream, self.version)
        ref_count = struct.unpack('<I', stream.read(4))[0]
        self.ref_list: List[Ref] = [Ref(stream, self.version) for _ in range(ref_count)]
        self.unk6 = struct.unpack('<f', stream.read(4))[0]
        self.unk7 = struct.unpack('<b', stream.read(1))[0]

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
