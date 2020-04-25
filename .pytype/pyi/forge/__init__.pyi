# (generated with --quick)

import forge.config.config_handler
import pathlib
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Type, Union

ConfigHandler: Type[forge.config.config_handler.ConfigHandler]
INTERNAL_PLUGIN_PATH: str
PLUGIN_BASE: Any
Path: Type[pathlib.Path]
PluginBase: Any
WORKING_DIR: str
os: module
sys: module

class Application:
    __doc__: str
    name: str
    plugin_source: Any
    plugins: List[str]
    registry: Dict[str, Tuple[Any, str]]
    def __init__(self, name: str, config_handler: forge.config.config_handler.ConfigHandler) -> None: ...
    def execute(self, command: str, args) -> None: ...
    def print_help(self) -> None: ...
    def register_plugin(self, name: str, plugin, helptext: str) -> None: ...

def main(args: list) -> None: ...
def tabulate(tabular_data: Union[Iterable[Iterable], Mapping[str, Iterable]], headers: Union[str, Sequence[str]] = ..., tablefmt: Union[str, tabulate.TableFormat] = ..., floatfmt: Union[str, Iterable[str]] = ..., numalign: Optional[str] = ..., stralign: Optional[str] = ..., missingval: Union[str, Iterable[str]] = ..., showindex: Union[bool, Iterable] = ..., disable_numparse: Union[bool, Iterable[int]] = ..., colalign: Optional[Iterable[Optional[str]]] = ...) -> str: ...
