import json
class Data:
    def __init__(self, vt, vn, p, s):
        self.vt = vt
        self.vn = vn
        self.p = p
        self.s = s

    @classmethod
    def from_json(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        res_p = []
        for key, values in data['p'].items():
            res_p.append(f'{key}->{"|".join(values)}')
        print(res_p)
        # Создаем экземпляр класса Data
        return cls(
            vt=' '.join(data['vt']),
            vn=' '.join(data['vn']),
            p=' '.join(res_p),
            s=data['s']
        )

def read_json():
    data = Data.from_json('data.json')
    return data.vt, data.vn, data.p, data.s
