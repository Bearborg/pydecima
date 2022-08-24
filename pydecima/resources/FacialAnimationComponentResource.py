from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion
import struct
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string

# TODO: Unfinished


class FacialAnimationComponentResource(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        start_pos = stream.tell()
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        self.head_grp_multimesh = Ref(stream, self.version)
        self.skeleton = Ref(stream, self.version)
        self.bone_bounding_boxes = Ref(stream, self.version)
        self.neutral_anim = Ref(stream, self.version)
        self.unk_ints = struct.unpack('<II', stream.read(8))[0]
        self.face_rig_data = Ref(stream, self.version)
        self.expressions = Ref(stream, self.version)
        # TODO
        stream.seek(start_pos)
        self.data = stream.read(self.size + 12)

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
