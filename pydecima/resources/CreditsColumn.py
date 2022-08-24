from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion
import struct
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string, read_utf16_chars


class CreditsColumn(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        name_len = struct.unpack('<I', stream.read(4))[0]
        self.credits_name = read_utf16_chars(stream, name_len)
        self.style = Ref(stream, self.version)
        self.style_2 = Ref(stream, self.version)
        self.unk = Ref(stream, self.version)
        assert self.unk.type == 0

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
