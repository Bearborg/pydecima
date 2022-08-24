import struct
from typing import BinaryIO, List
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.HumanoidBodyVariant import HumanoidBodyVariant
from pydecima.resources.HumanoidBodyVariantGroup import HumanoidBodyVariantGroup
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string


class SpawnSetup(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        self.graph_condition = Ref(stream, self.version)
        self.impostor = Ref(stream, self.version)
        self.humanoid = Ref(stream, self.version)
        self.graph_program = Ref(stream, self.version)
        self.faction = Ref(stream, self.version)
        unk_refs_1_count = struct.unpack('<I', stream.read(4))[0]
        self.unk_refs_1: List[Ref] = [Ref(stream, self.version) for _ in range(unk_refs_1_count)]
        unk_refs_2_count = struct.unpack('<I', stream.read(4))[0]
        self.unk_refs_2: List[Ref] = [Ref(stream, self.version) for _ in range(unk_refs_2_count)]
        self.unk_ints = struct.unpack('<iii', stream.read(12))
        self.unk_byte = struct.unpack('<b', stream.read(1))
        unk_refs_3_count = struct.unpack('<I', stream.read(4))[0]
        self.unk_refs_3: List[Ref] = [Ref(stream, self.version) for _ in range(unk_refs_3_count)]
        self.inventory_collection = Ref(stream, self.version)
        self.combat_behavior = Ref(stream, self.version)
        self.humanoid_body_variant: [Ref[HumanoidBodyVariant], Ref[HumanoidBodyVariantGroup]] =\
            Ref(stream, self.version)
        self.combat_properties = Ref(stream, self.version)
        self.combat_properties_facts = Ref(stream, self.version)

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
