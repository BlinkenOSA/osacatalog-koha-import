# coding=utf-8
from hashids import Hashids
from pymarc import MARCReader, Field
import os

inputdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
outputdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')

m580a = {
    'VargaLaszlo':          u'Donation of László Varga',
    'OSIBudapest':          u'HU OSA 207 - Donation of the Open Society Institute–Budapest',
    'OSINewYork':           u'HU OSA 208 - Donation of the Open Society Institute–New York',
    'RFE/RLcoll':           u'HU OSA 300 - RFE/RL collection',
    'RegionalPress':        u'HU OSA 300-85-18 - Regional Press',
    'InformalPress':        u'HU OSA 300-85-19 - Informal Press',
    'IHRLI':                u'HU OSA 304 - International Human Rights Law Institute collection',
    'ReischAlfred':         u'HU OSA 312 - Donation of Alfred A. Reisch',
    'IHFcoll':              u'HU OSA 318 - Donation of the International Helsinki Federation for Human Rights',
    'FicVictor':            u'HU OSA 385 - Donation of Victor M. Fic',
    'InstPublicOpinion':    u'HU OSA 420 - Hungarian Institute for Public Opinion Research collection',
    'RepPress':             u"Republics' Press",
    'SamizdatEmigre':       u'Samizdat and Emigré Publications',
    'Magos':                u'HU OSA 416 - Donation of Gábor Magos',
    'KemenyIstvan':         u'HU OSA 368 - Donation of István Kemény',
    'LGI':                  u'HU OSA 104 - Donation of the Local Government and Public Service Reform Initiative',
    'HegedusAndras':        u'HU OSA 361 - Donation of Hegedüs András'
}

alphanum_reverse_map = {
    '0': 'Z',
    '1': 'Y',
    '2': 'X',
    '3': 'W',
    '4': 'V',
    '5': 'U',
    '6': 'T',
    '7': 'S',
    '8': 'R',
    '9': 'Q',
    'A': 'P',
    'B': 'O',
    'C': 'N',
    'D': 'M',
    'E': 'L',
    'F': 'K',
    'G': 'J',
    'H': 'I',
    'I': 'H',
    'J': 'G',
    'K': 'F',
    'L': 'E',
    'M': 'D',
    'N': 'C',
    'O': 'B',
    'P': 'A',
    'Q': '9',
    'R': '8',
    'S': '7',
    'T': '6',
    'U': '5',
    'V': '4',
    'W': '3',
    'X': '2',
    'Y': '1',
    'Z': '0'
}

def main():
    for file in os.listdir(inputdir):
        if file.endswith(".mrc"):
            counter = 0

            inputfile = os.path.join(inputdir, file)
            outputfile = os.path.join(outputdir, file)

            if os.path.exists(outputfile):
                os.remove(outputfile)

            hashids = Hashids(salt="osalibrary", min_length=8)

            with open(inputfile, 'rb') as fh:
                print "Reading file: " + inputfile
                reader = MARCReader(fh)
                for record in reader:
                    id = long(record['999']['c'])

                    record.add_field(
                        Field(
                            tag = '920',
                            indicators = ['0','1'],
                            subfields = [
                                'a', hashids.encode(id)
                            ]))

                    for f in record.get_fields('580'):
                        if f.subfields[1] in m580a.keys():
                            f.subfields[1] = m580a[f.subfields[1]]
                        else:
                            record.remove_field(f)

                    try:
                        callnum = record['952']['6']
                        if callnum:
                            revcallnum = reverse_call_number(callnum)

                            record.add_field(
                                Field(
                                    tag = '992',
                                    indicators = ['0','1'],
                                    subfields = [
                                        'a', callnum,
                                        'b', revcallnum
                                    ]))

                        restricted = record['952']['5']

                        if restricted != '1':
                            out = open(outputfile, 'ab')
                            out.write(record.as_marc())
                            out.close()
                            counter += 1

                    except TypeError:
                        print "There is something wrong with Type or Call Number value in record: %s - I skip that from this batch!" % (id)

                print "Saved: " + outputfile

            with open(outputfile, 'rb') as fh:
                reader = MARCReader(fh)
                for record in reader:
                    print 'Added hashid: ' + record['920']['a']
                    for f in record.get_fields('992'):
                        print 'Call number: ' + f.subfields[1].encode('utf-8')
                        print 'Reverse Call number: ' + f.subfields[3].encode('utf-8')

            print "Total number of records: " + str(counter)


def reverse_call_number(call_number):
    rev = ""
    for c in call_number:
        if c in alphanum_reverse_map:
            rev += alphanum_reverse_map[str(c)]
        else:
            rev += c
    return rev

if __name__ == "__main__":
    main()
