import struct
from typing import BinaryIO, List
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.LocalizedTextResource import LocalizedTextResource
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string


class FocusScannedInfo(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        self.title: Ref[LocalizedTextResource] = Ref(stream, self.version)
        self.description_alternate: Ref[LocalizedTextResource] = Ref(stream, self.version)
        self.description: Ref[LocalizedTextResource] = Ref(stream, self.version)
        self.target_type = Ref(stream, self.version)
        category_count = struct.unpack('<I', stream.read(4))[0]
        self.categories: List[Ref] = [Ref(stream, self.version) for _ in range(category_count)]
        self.scannable_body = Ref(stream, self.version)
        self.outlineSettings = Ref(stream, self.version)
        property_count = struct.unpack('<I', stream.read(4))[0]
        self.properties: List[Ref] = [Ref(stream, self.version) for _ in range(property_count)]
        self.graph_condition = Ref(stream, self.version)

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
