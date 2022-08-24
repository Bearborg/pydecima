import struct
from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.FocusScannedInfo import FocusScannedInfo
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string


class FocusTargetComponentResource(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        self.boolean_fact = Ref(stream, self.version)
        self.unk_short_1 = struct.unpack('<h', stream.read(2))[0]
        self.unk_short_2 = struct.unpack('<h', stream.read(2))[0]
        self.unk_int_1 = struct.unpack('<I', stream.read(4))[0]
        assert self.unk_int_1 == 0
        self.unk_float = struct.unpack('<f', stream.read(4))[0]
        self.unk_byte_1 = struct.unpack('<b', stream.read(1))[0]
        assert self.unk_byte_1 == 0
        self.focus_scanned_info: Ref[FocusScannedInfo] = Ref(stream, self.version)
        unk_ref_count = struct.unpack('<I', stream.read(4))[0]
        self.unk_ref_list = [Ref(stream, self.version) for _ in range(unk_ref_count)]
        self.unk_byte_2 = struct.unpack('<b', stream.read(1))[0]
        self.focus_tracking_path_entity = Ref(stream, self.version)

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
