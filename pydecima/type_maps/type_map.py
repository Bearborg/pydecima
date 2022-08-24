from .pc_type_map import pc_type_map
from .ps4_type_map import ps4_type_map
from .dspc_type_map import dspc_type_map
from pydecima.enums.DecimaVersion import DecimaVersion


def get_type_map(version: DecimaVersion):
    if version == DecimaVersion.HZDPC:
        return pc_type_map
    elif version == DecimaVersion.HZDPS4:
        return ps4_type_map
    elif version == DecimaVersion.DSPC:
        return dspc_type_map
    else:
        raise Exception(f"No matching type map found for {version}")
