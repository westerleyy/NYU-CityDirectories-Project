
class PersonalNames:

    def __init__(self):
        self.personalnames = [i.lower().rstrip('\n') for i \
                         in list(set(open('/Volumes/ds_staff/RDM_nypl_directories/city-directory-entry-parser/data/known-entity-dictionaries/IPUMS-1880-10-Names.txt').readlines()))]

        self.nameindex = {}
        for m in self.personalnames:
            try:
                self.nameindex[m[0:2]].append(m)
            except KeyError:
                self.nameindex[m[0:2]] = []
                self.nameindex[m[0:2]].append(m)

    def checkname(self, input):
        return self.nameindex[input[0:2].lower()]

class OccupationNames:

    def __init__(self):
        self.occnames = [i.lower().rstrip('\n') for i \
                         in list(set(open('/Volumes/ds_staff/RDM_nypl_directories/city-directory-entry-parser/data/known-entity-dictionaries/occwors.txt').readlines()))]

        self.occindex = {}
        for m in self.occnames:
            try:
                self.occindex[m[0:2]].append(m)
            except KeyError:
                self.occindex[m[0:2]] = []
                self.occindex[m[0:2]].append(m)

    def checkocc(self, input):
        return self.occindex[input[0:2].lower()]


class StreetNames:

    def __init__(self):
        self.streetnames = [i.lower().replace('(','').rstrip('\n') for i \
                         in list(set(open('/Volumes/ds_staff/RDM_nypl_directories/city-directory-entry-parser/data/known-entity-dictionaries/streetnames.txt').readlines()))]

        self.streetindex = {}
        for m in self.streetnames:
            try:
                self.streetindex[m[0]].append(m)
            except KeyError:
                self.streetindex[m[0]] = []
                self.streetindex[m[0]].append(m)
            except IndexError:
                pass

    def checkstreet(self, input):
        return self.streetindex[input[0].lower()]
