"""
Cifrado y descrifado de ID por medio de Hashids
"""
from typing import Any
import re
from hashids import Hashids

from config.settings import SALT

hashids = Hashids(SALT, min_length=8)
hashid_regexp = re.compile("[0-9a-zA-Z]{8,16}")


def cifrar_id(un_id: int) -> str:
    """Cifrar ID"""
    return hashids.encode(un_id)


def descifrar_id(un_id_hasheado: str) -> Any:
    """Descifrar ID"""
    if hashid_regexp.match(un_id_hasheado):
        un_id_descifrado = hashids.decode(un_id_hasheado)
        if len(un_id_descifrado) == 1:
            return un_id_descifrado[0]
    return None
