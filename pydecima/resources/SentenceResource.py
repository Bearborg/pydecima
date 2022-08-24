import struct
from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.LocalizedSimpleSoundResource import LocalizedSimpleSoundResource
from pydecima.resources.LocalizedTextResource import LocalizedTextResource
from pydecima.resources.VoiceResource import VoiceResource
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string


# TODO: Unfinished
class SentenceResource(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        self.unk_int = struct.unpack('<I', stream.read(4))[0]
        self.unk_byte_1 = struct.unpack('<b', stream.read(1))[0]
        self.unk_byte_2 = struct.unpack('<b', stream.read(1))[0]
        self.sound: Ref[LocalizedSimpleSoundResource] = Ref(stream, self.version)
        self.animation: Ref = Ref(stream, self.version)
        self.text: Ref[LocalizedTextResource] = Ref(stream, self.version)
        self.voice: Ref[VoiceResource] = Ref(stream, self.version)

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
