import struct
from typing import BinaryIO, List
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string


class HumanoidBodyVariant(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        self.model_part = Ref(stream, self.version)
        self.ability_pose_deformer = Ref(stream, self.version)
        unk_refs_1_count = struct.unpack('<I', stream.read(4))[0]
        self.unk_refs_1: List[Ref] = [Ref(stream, self.version) for _ in range(unk_refs_1_count)]
        unk_refs_2_count = struct.unpack('<I', stream.read(4))[0]
        self.unk_refs_2: List[Ref] = [Ref(stream, self.version) for _ in range(unk_refs_2_count)]
        unk_refs_3_count = struct.unpack('<I', stream.read(4))[0]
        self.unk_refs_3: List[Ref] = [Ref(stream, self.version) for _ in range(unk_refs_3_count)]
        self.unk_ref_4 = Ref(stream, self.version)
        self.unk_int_5 = struct.unpack('<I', stream.read(4))[0]
        self.unk_ref_6 = Ref(stream, self.version)
        self.unk_int_7 = struct.unpack('<I', stream.read(4))[0]
        self.unk_float_8 = struct.unpack('<f', stream.read(4))[0]
        unk_refs_9_count = struct.unpack('<I', stream.read(4))[0]
        self.unk_refs_9: List[Ref] = [Ref(stream, self.version) for _ in range(unk_refs_9_count)]
        unk_strings_10_count = struct.unpack('<I', stream.read(4))[0]
        self.unk_strings_10: List[str] = [parse_hashed_string(stream) for _ in range(unk_strings_10_count)]

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
