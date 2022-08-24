import io
from typing import BinaryIO, List
from pydecima.enums.DecimaVersion import DecimaVersion
import struct
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string


class MusicResource(Resource):
    class FourCCTableEntry:
        def __init__(self, stream: BinaryIO):
            self.name = stream.read(4).decode('ascii')
            self.offset = struct.unpack("<I", stream.read(4))[0]
            self.size = struct.unpack("<I", stream.read(4))[0]

    class MEDASectionEntry:
        def __init__(self, stream: BinaryIO):
            self.offset = struct.unpack("<Q", stream.read(8))[0]
            self.size = struct.unpack("<Q", stream.read(8))[0]
            self.unk = [struct.unpack("<I", stream.read(4))[0] for _ in range(8)]

    class MEDASection:
        def __init__(self, stream: BinaryIO):
            self.magic = stream.read(4).decode('ascii')
            assert self.magic == 'PICD', "Magic != PICD"
            offsets_size = struct.unpack("<I", stream.read(4))[0]
            stream.read(8)  # padding?
            self.offsets: List[MusicResource.MEDASectionEntry] =\
                [MusicResource.MEDASectionEntry(stream) for _ in range(offsets_size)]

    class SectionStruct:
        def __init__(self, stream: BinaryIO):
            start_pos = stream.tell()
            fourcc_table_start_pos = start_pos + 12
            self.fourcc_table = [MusicResource.FourCCTableEntry(stream)]
            assert self.fourcc_table[0].name == "ECHO", "First entry wasn't ECHO"

            while stream.tell() - fourcc_table_start_pos < self.fourcc_table[0].size:
                self.fourcc_table.append(MusicResource.FourCCTableEntry(stream))
            self.sections = {}
            for section in self.fourcc_table:
                stream.seek(section.offset)
                if section.name == "MEDA":
                    self.sections[section.name] = MusicResource.MEDASection(stream)
                elif section.name == "STRL":
                    self.sections[section.name] = stream.read(section.size).decode('ascii').split('\00')[:-1]
                else:
                    self.sections[section.name] = stream.read(section.size)

    class CacheStruct:
        def __init__(self, stream: BinaryIO):
            cache_string_length = struct.unpack("<I", stream.read(4))[0]
            self.cache_string = stream.read(cache_string_length).decode('ascii')
            self.unk1 = struct.unpack("<I", stream.read(4))[0]
            self.unk2 = struct.unpack("<I", stream.read(4))[0]
            self.file_size = struct.unpack("<I", stream.read(4))[0]
            self.unk3 = struct.unpack("<I", stream.read(4))[0]

    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        unk1_count = struct.unpack("<I", stream.read(4))[0]
        self.unk1 = [struct.unpack("<I", stream.read(4))[0] for _ in range(unk1_count)]
        self.unk2 = struct.unpack("<I", stream.read(4))[0]
        self.unk3 = struct.unpack("<B", stream.read(1))[0]
        self.unk4 = struct.unpack("<i", stream.read(4))[0]
        submix_count = struct.unpack("<I", stream.read(4))[0]
        self.submixes = []
        for _ in range(submix_count):
            submix_name = parse_hashed_string(stream)
            submix_ref = Ref(stream, self.version)
            self.submixes.append((submix_name, submix_ref))
        chunk_name_count = struct.unpack("<I", stream.read(4))[0]
        self.chunk_names = [parse_hashed_string(stream) for _ in range(chunk_name_count)]
        section_struct_size = struct.unpack("<I", stream.read(4))[0]
        self.section_struct = MusicResource.SectionStruct(io.BytesIO(stream.read(section_struct_size)))
        self.cache_structs = [MusicResource.CacheStruct(stream) for _ in range(chunk_name_count)]

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)

    def __repr__(self):
        return self.__str__()
