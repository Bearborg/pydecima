import struct
from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.LocalizedTextResource import LocalizedTextResource
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string


class VoiceResource(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        self.unk_1 = stream.read(4)
        self.unk_2 = struct.unpack('<b', stream.read(1))[0]
        self.text: Ref[LocalizedTextResource] = Ref(stream, self.version)

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
