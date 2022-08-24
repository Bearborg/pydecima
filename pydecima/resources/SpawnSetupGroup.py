import struct
from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.Resource import Resource
from pydecima.resources.SpawnSetup import SpawnSetup
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string


class SpawnSetupGroup(Resource):
    class UnkStruct:
        def __init__(self, stream: BinaryIO, version: DecimaVersion):
            self.unk_float = struct.unpack('<f', stream.read(4))[0]
            self.unk_ref: [Ref[SpawnSetup], Ref[SpawnSetupGroup]] = Ref(stream, version)

    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        self.unk_boolean_fact = Ref(stream, self.version)
        self.unk2 = Ref(stream, self.version)
        assert self.unk2.type == 0
        unk_struct_count = struct.unpack('<I', stream.read(4))[0]
        self.unk_structs = [SpawnSetupGroup.UnkStruct(stream, self.version) for _ in range(unk_struct_count)]

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
