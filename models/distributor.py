from typing import Any
from dataclasses import dataclass
import json


@dataclass
class Distributor:
    id: str
    nama: str
    lokasi: str

    @staticmethod
    def from_dict(obj: Any) -> 'Distributor':
        _id = str(obj.get("id"))
        _nama = str(obj.get("nama"))
        _lokasi = str(obj.get("lokasi"))
        return Distributor(_id, _nama, _lokasi)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
