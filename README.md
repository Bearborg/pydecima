# PyDecima

This package contains a reader utility for .core files used by the Decima game engine, intended for use in exporting
assets and datamining. Using PyDecima, resources from one or multiple Decima .cores can be deserialized into Python
objects and loaded into a dictionary to enable lookup by their identifier UUID, as well as simple following of
cross-file references.

## Examples

### Initialization
The primary use of this package is through the `reader` module, which can be used in a script like so:

```python
import pydecima

output_dict = {}
pydecima.reader.set_globals(_game_root=r'C:\HZD_extracted_files', _decima_version='HZDPC')
pydecima.reader.read_objects(r'C:\HZD_extracted_files\localized\sentences\aigenerated\aloy\sentences.core', output_dict)
```

The above script will populate the `output_dict` variable with all the resources contained inside the specified .core.
`_decima_version` accepts values of "HZDPC" (default), "HZDPS4", or "DSPC", although currently there is very little
support for Death Stranding resource formats. `_game_root` should be set to the root of your extracted Decima files,
and is necessary to enable reference following. An alternative parameter, `_game_root_file`, can be used, which expects
a plaintext file containing only the path that would normally be passed into `_game_root`. This can be convenient for
scripts, since the root path can be stored in a persistent file instead of being entered by the user at runtime.

### Parsing resources
With the `output_dict` variable populated, we can easily iterate through the resources in a .core and read some data.

```python
from pydecima.resources import SentenceResource
from pydecima.enums import ETextLanguages

for resource in output_dict.values():
    if isinstance(resource, SentenceResource):
        localized_text = resource.text.follow(output_dict)
        if localized_text is not None:
            print(f'{resource.name}: {localized_text.language[ETextLanguages.English]}')
```

The above script will produce a printout of every subtitled line in a dialogue file, prefaced by its internal name.