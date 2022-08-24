import struct
from codecs import iterdecode
from functools import partial
from itertools import islice
from typing import BinaryIO

from pydecima.resources.structs.HashedString import HashedString


def parse_hashed_string(stream: BinaryIO, include_hash=False):
    size = struct.unpack('<I', stream.read(4))[0]
    if size > 0:
        string_hash = stream.read(4)
    else:
        string_hash = bytes()
    if include_hash:
        return HashedString(string_hash, stream.read(size).decode('ASCII'))
    else:
        return stream.read(size).decode('ASCII')


def read_utf16_chars(stream: BinaryIO, length):
    # Read one byte at a time
    binary_chunks = iter(partial(stream.read, 1), "")
    # Convert bytes into unicode code points
    decoder = iterdecode(binary_chunks, 'utf_16_le')
    return str().join(islice(decoder, length))
