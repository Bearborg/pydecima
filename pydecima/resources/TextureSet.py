import struct
from typing import BinaryIO, List
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.enums.ETextureSetType import ETextureSetType
from pydecima.resources.Resource import Resource
from pydecima.resources.Texture import Texture
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string


class TextureSet(Resource):
    class TextureDetails:
        class ChannelDetails:
            def __init__(self, stream: BinaryIO):
                channel_details = struct.unpack('<B', stream.read(1))[0]
                self.setType: ETextureSetType = ETextureSetType(channel_details & 0x0F)
                self.unk = channel_details >> 4

        def __init__(self, stream: BinaryIO, version):
            self.unk_int1 = struct.unpack('<I', stream.read(4))[0]
            self.unk_int2 = struct.unpack('<I', stream.read(4))[0]
            self.unk_byte = struct.unpack('<b', stream.read(1))
            self.channel_details: List[TextureSet.TextureDetails.ChannelDetails] = \
                [self.ChannelDetails(stream) for _ in range(4)]
            self.unk_int3 = struct.unpack('<I', stream.read(4))[0]
            self.texture: Ref[Texture] = Ref(stream, version)

    class SourceDetails:
        def __init__(self, stream: BinaryIO):
            set_type_int = struct.unpack('<I', stream.read(4))[0]
            self.set_type: ETextureSetType = ETextureSetType(set_type_int)
            self.source_filename = parse_hashed_string(stream)
            self.unk_byte1 = struct.unpack('<b', stream.read(1))
            self.unk_byte2 = struct.unpack('<b', stream.read(1))
            self.unk_int1 = struct.unpack('<I', stream.read(4))[0]
            self.unk_int2 = struct.unpack('<I', stream.read(4))[0]
            self.unk_int3 = struct.unpack('<I', stream.read(4))[0]
            self.width = struct.unpack('<I', stream.read(4))[0]
            self.height = struct.unpack('<I', stream.read(4))[0]
            self.unk_float1 = struct.unpack('<f', stream.read(4))[0]
            self.unk_float2 = struct.unpack('<f', stream.read(4))[0]
            self.unk_float3 = struct.unpack('<f', stream.read(4))[0]
            self.unk_float4 = struct.unpack('<f', stream.read(4))[0]

    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        texture_count = struct.unpack('<I', stream.read(4))[0]
        self.textures = [self.TextureDetails(stream, version) for _ in range(texture_count)]
        self.unk_int1 = struct.unpack('<I', stream.read(4))[0]
        assert self.unk_int1 == 0
        source_count = struct.unpack('<I', stream.read(4))[0]
        self.sources = [self.SourceDetails(stream) for _ in range(source_count)]

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
