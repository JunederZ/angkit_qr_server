
class DistributorModel:

    def __init__(self, data):

        self.nama = data[0]
        self.lokasi = data[1]
        self.id = data[2]

    def getData(self):
        return {
            "nama": self.nama,
            "lokasi": self.lokasi,
            "id": self.id
        }

    def getTuple(self):
        return self.nama, self.lokasi, self.id