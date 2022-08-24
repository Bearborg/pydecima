import struct
from typing import BinaryIO, List
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.LocalizedTextResource import LocalizedTextResource
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string


class InventoryItemComponentResource(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        self.item_name: Ref[LocalizedTextResource] = Ref(stream, self.version)
        self.item_description: Ref[LocalizedTextResource] = Ref(stream, self.version)
        self.item_price_info = Ref(stream, self.version)
        self.unk = struct.unpack('<I', stream.read(4))[0]
        self.item_icon = Ref(stream, self.version)
        self.item_icon_2 = Ref(stream, self.version)
        self.broken_ref = Ref(stream, self.version)
        self.unk_ref = Ref(stream, self.version)
        self.unk_ref2 = Ref(stream, self.version)
        self.unk_ref3 = Ref(stream, self.version)
        ref_count = struct.unpack('<I', stream.read(4))[0]
        self.ref_list: List[Ref] = [Ref(stream, self.version) for _ in range(ref_count)]
        self.unk_short = struct.unpack('<H', stream.read(2))[0]
        ref_count_2 = struct.unpack('<I', stream.read(4))[0]
        self.ref_list_2: List[Ref] = [Ref(stream, self.version) for _ in range(ref_count_2)]
        stream.read(5)  # TODO
        self.soundbank = Ref(stream, self.version)
        self.unk_ref3 = Ref(stream, self.version)
        stream.read(2)  # TODO
