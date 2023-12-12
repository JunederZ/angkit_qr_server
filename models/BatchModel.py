
import datetime

class BatchModel:

    def __init__(self, data):

        self.id = data[0]
        self.jenisTernak = data[1]
        self.peternak = data[2]
        self.distributor = data[3]
        self.beratRata = data[4]
        self.tanggalMulai = data[5].isoformat()
        self.tanggalPotong = data[6].isoformat()
        self.tanggalKemas = data[7].isoformat()

    def getData(self):
        return {
            "id": self.id,
            "jenisTernak": self.jenisTernak,
            "peternak": self.peternak.getData(),
            "distributor": self.distributor.getData(),
            "beratRata": self.beratRata,
            "tanggalMulai": self.tanggalMulai,
            "tanggalPotong": self.tanggalPotong,
            "tanggalKemas": self.tanggalKemas,
        }