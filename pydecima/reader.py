import io
import os
import struct
import binascii
from typing import Dict
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources import Resource, UnknownResource
from pydecima.type_maps import get_type_map
import pydecima.resources
import inspect

defined_resource_types = [member[0] for member in inspect.getmembers(pydecima.resources)]
game_root: str = ""
decima_version: DecimaVersion = DecimaVersion.HZDPC
use_buffering: bool = False


def set_globals(*, _game_root=None, _game_root_file=None, _decima_version=None, _use_buffering=None):
    global game_root
    global decima_version
    global use_buffering

    if type(_game_root) == str and type(_game_root_file) == str:
        raise ValueError("_game_root and _game_root_file cannot both be specified")
    elif type(_game_root) == str:
        assert os.path.isdir(_game_root), "_game_root is not a valid directory"
        game_root = _game_root
    elif type(_game_root_file) == str:
        assert os.path.isfile(_game_root_file), "_game_root_file is not a valid file"
        root_file_contents = open(_game_root_file, 'r').read().strip('" \t\r\n')
        assert os.path.isdir(root_file_contents), "_game_root_file does not contain a path to a valid directory"
        game_root = root_file_contents

    if type(_decima_version) == DecimaVersion:
        decima_version = _decima_version
    elif type(_decima_version) == str:
        version = DecimaVersion(_decima_version.upper())
        decima_version = version

    if type(_use_buffering) == bool:
        use_buffering = _use_buffering


def read_objects(in_file_name: str, out_dict: Dict[bytes, Resource]):
    with open(in_file_name, 'rb') as in_file:
        try:
            return read_objects_from_stream(io.BytesIO(in_file.read()), out_dict)
        except Exception as e:
            raise Exception(f'Error in {in_file_name}: {e}')


def read_objects_from_stream(in_file: io.BytesIO, out_dict: Dict[bytes, Resource]):
    type_map = get_type_map(decima_version)

    while True:
        start_pos = in_file.tell()
        if not in_file.read(1):
            break
        in_file.seek(start_pos)
        type_hash, size = struct.unpack('<QI', in_file.read(12))
        in_file.seek(start_pos)
        if use_buffering:
            stream = io.BytesIO(in_file.read(12 + size))
        else:
            stream = in_file
        # check type map to see if we have a dedicated constructor
        little_endian_type = '{0:X}'.format(type_hash)
        type_name: str = "Unknown"
        if little_endian_type in type_map:
            type_name = type_map[little_endian_type]

        parse_start_pos = stream.tell()

        if type_name in defined_resource_types:
            try:
                specific_res = eval(f'pydecima.resources.{type_name}(stream, decima_version)')
                out_dict[specific_res.uuid] = specific_res
                parse_end_pos = stream.tell()
                read_count = (parse_end_pos - parse_start_pos)
                if size + 12 != read_count:
                    raise Exception("{} {} didn't match size, expected {}, read {}"
                          .format(specific_res.type, binascii.hexlify(specific_res.uuid).decode('ASCII'),
                                  size + 12, read_count))
            except Exception as e:
                stream.seek(parse_start_pos)
                unknown_res = UnknownResource(stream, decima_version)
                raise Exception("{} {} failed to parse, error: {}"
                                .format(type_name, binascii.hexlify(unknown_res.uuid).decode('ASCII'), e))
        else:
            unknown_res = UnknownResource(stream, decima_version)
            out_dict[unknown_res.uuid] = unknown_res
