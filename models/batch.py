from dataclasses import dataclass, asdict
import json


@dataclass
class Batch:
    berat_rt: float
    distributor: str
    id: str
    jenis_ternak: str
    peternak: str
    tgl_kemas: str
    tgl_mulai: str
    tgl_potong: str

    @staticmethod
    def from_json(jsn: str) -> 'Batch':
        obj = json.loads(jsn)
        _berat_rt = float(obj.get("beratRata"))
        _distributor = str(obj.get("distributor"))
        _id = str(obj.get("id"))
        _jenis_ternak = str(obj.get("jenisTernak"))
        _peternak = str(obj.get("peternak"))
        _tgl_kemas = str(obj.get("tanggalKemas"))
        _tgl_mulai = str(obj.get("tanggalMulai"))
        _tgl_potong = str(obj.get("tanggalPotong"))
        return Batch(_berat_rt, _distributor, _id, _jenis_ternak, _peternak, _tgl_kemas, _tgl_mulai, _tgl_potong)

    def to_json(self) -> str:
        return json.dumps(asdict(self))


j = '''{
  "beratRata": 9.2,
  "distributor": "FOREIGN KEY DISTRIBUTOR",
  "id": "000001",
  "jenisTernak": "Jakarta",
  "peternak": "FOREIGN KEY PETERNAKAN",
  "tanggalKemas": "DATE IN ISO FORMAT",
  "tanggalMulai": "DATE IN ISO FORMAT",
  "tanggalPotong": "DATE IN ISO FORMAT"
}'''


b = Batch.from_json(j)
print(b)
print(b.to_json())


