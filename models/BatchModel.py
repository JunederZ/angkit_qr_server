
class BatchModel:

    def __init__(self, jsonData: dict):

        self.peternak = jsonData['peternak']
        self.distributor = jsonData['distributor']
        self.beratRata = jsonData['berat_rt_sample']
        self.tanggalMulai = jsonData['tgl_mulai']
        self.tanggalPotong = jsonData['tgl_potong']
        self.tanggalKemas = jsonData['tgl_kemas']
        self.id = jsonData['id']
        self.jenisTernak = jsonData['jenis_ternak']

