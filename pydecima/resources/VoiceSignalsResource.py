import struct
from typing import BinaryIO, List
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.Resource import Resource
from pydecima.resources.SentenceResource import SentenceResource
from pydecima.resources.VoiceResource import VoiceResource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string


class VoiceSignalsResource(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        self.voice: Ref[VoiceResource] = Ref(stream, self.version)
        sentences_count = struct.unpack('<I', stream.read(4))[0]
        self.sentences: List[Ref[SentenceResource]] = [Ref(stream, self.version) for _ in range(sentences_count)]

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
