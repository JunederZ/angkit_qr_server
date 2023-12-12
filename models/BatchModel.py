
class BatchModel:

    def __init__(self, data):

        # self.id = data['id']
        # self.jenisTernak = data['jenis_ternak']
        # self.peternak = data['peternak']
        # self.distributor = data['distributor']
        # self.beratRata = data['berat_rt_sample']
        # self.tanggalMulai = data['tgl_mulai']
        # self.tanggalPotong = data['tgl_potong']
        # self.tanggalKemas = data['tgl_kemas']

        self.id = data[0]
        self.jenisTernak = data[1]
        self.peternak = data[2]
        self.distributor = data[3]
        self.beratRata = data[4]
        self.tanggalMulai = data[5]
        self.tanggalPotong = data[6]
        self.tanggalKemas = data[7]

    def getData(self):
        return {
            "id": self.id,
            "jenisTernak": self.jenisTernak,
            "peternak": self.peternak,
            "distributor": self.distributor,
            "beratRata": self.beratRata,
            "tanggalMulai": self.tanggalMulai,
            "tanggalPotong": self.tanggalPotong,
            "tanggalKemas": self.tanggalKemas,
        }