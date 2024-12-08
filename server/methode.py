class allin:
    def __init__(self):
        self.data = {"data": []}

    def add(self, results):
        """Tambah data prediksi ke dalam objek."""
        for item in results:
            data_item = {
                "id": item[0],
                "predicted_class": item[1],
                "confidence": item[2]
            }
            self.data["data"].append(data_item)
