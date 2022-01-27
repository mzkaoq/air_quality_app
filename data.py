import collections

class ConreteProbe:
    def __init__(self,id,name,cord_x,cord_y,voivodeship):
        self.id = id
        self.name = name
        self.cord_x = cord_x
        self.cord_y = cord_y
        self.voivodeship = voivodeship
        self.data = {}
        self.average_24h = None
        self.average_72h = None

    def add_new_data(self,code,value):
        self.data[code]=value

    def update_averages(self):
        sorted_dict = collections.OrderedDict(sorted(self.data.items()))
        records = list(sorted_dict.items())
        suma = 0
        for value in records[-24:]:
            suma += value[1]
        self.average_24h = suma/24
        suma = 0
        for value in records[-72:]:
            suma += value[1]
        self.average_72h = suma/72

    def return_average(self):
        return (self.average_24h,self.average_72h)

    def return_list(self):
        sorted_dict = collections.OrderedDict(sorted(self.data.items()))
        records = list(sorted_dict.items())
        list24 = records[-24:]
        new_list24 = []
        hours24=[]
        hours72=[]
        data24=[]

        for elem in list24:
            hours24 = []
            data24 = []
            elem=list(elem)
            modified_elem = str(elem[0])
            elem[0] = modified_elem[8:10]
            new_list24.append((int(modified_elem[8:10]),elem[1]))
            for element in new_list24:
                hours24.append(str(element[0]))
                data24.append(element[1])
        return [(hours24,data24)]

    def return_all_data(self):
        return self.data

class ProbeManager:
    def __init__(self):
        self.all_probes = []

    def add_probe(self,probe):
        self.all_probes.append(probe)

    def return_list(self):
        return self.all_probes

    def return_concrete_probe(self,concrete_id):
        for elem in self.all_probes:
            if elem.id == int(concrete_id):
                return elem

    def erase_data(self):
        self.all_probes = []






