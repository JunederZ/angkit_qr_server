
class DistributorModel:

    def __init__(self, jsonData: dict):

        self.namaDistributor = jsonData['nama']
        self.lokasiDistributor = jsonData['lokasi']
        self.id = jsonData['id']
