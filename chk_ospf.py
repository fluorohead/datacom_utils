import sys, os, re
from stat import S_ISDIR

def WorkWithFile(strFN):
    dictResult = {'ospf': True, 'ldp': True, 'mcast': True, 'pim': True}
    strPartEnding = '!\n'
    strStrip = 'interface '
    #print(f'file > {strFN}')
    try:
        fileIn = open(strFN, mode = 'rt')
    except:
        print('Error opening!', file = sys.stderr)
        dictResult = {'ospf' : False, 'ldp' : False, 'mcast' : False, 'pim' : False}
    else:
        #print('Opening Ok')
        list_OSPFInterfaces = []
        for strLine in fileIn: # searching for 'router ospf' beginning
            if re.match('^router ospf \d{1,5}$\n', strLine):
                #print('router ospf pattern found')
                break
        for strLine in fileIn: # searching for router ospf 1 ending
            if strLine != strPartEnding:
#                print(strLine, end = '')
                if re.match('^ {2}interface.*', strLine) and (not re.match('.*Loopback.*', strLine)):
                    list_OSPFInterfaces.append(strLine.strip().lstrip(strStrip))
            else:
                break
        if list_OSPFInterfaces:
            #print(f'OSPF : {list_OSPFInterfaces}')
            def FindPartition(strRegexp, strInterface, strExclude):
                flagPresent = False
                listInterfaces = []
                for strLine2 in fileIn:
                    if re.match(strRegexp, strLine2):
                        flagPresent = True
                        break
                if flagPresent:
                    for strLine2 in fileIn:
                        if strLine2 != strPartEnding:
                            if re.match(strInterface, strLine2):
                                listInterfaces.append(strLine2.strip().strip(strStrip))
                        else:
                            break
                else:
                    fileIn.seek(0)
                return listInterfaces
            list_LDPInterfaces = FindPartition('^mpls ldp$', '^ interface.*')
            list_MCASTInterfaces = FindPartition('^multicast-routing$\n', '^ {2}interface.*')
            list_PIMInterfaces = FindPartition('^router pim$\n', '^ {2}interface.*')
            # main searching
            for strZ in list_OSPFInterfaces:
                if strZ not in list_LDPInterfaces:
                    dictResult['ldp'] = False
                if strZ not in list_MCASTInterfaces:
                    dictResult['mcast'] = False
                if strZ not in list_PIMInterfaces:
                    dictResult['pim'] = False
        else:
            dictResult = {'ospf': False, 'ldp': False, 'mcast': False, 'pim': False}
            #print('No interfaces found in \'router ospf\' partition.')
        fileIn.close()
    finally:
        #print(f'Result dict : {dictResult}')
        return dictResult


def RecursiveFileSearch(strTop):
    #print(f'dir > {strTop}')
    for strNext in os.listdir(strTop):
        strNextSearchIn = f'{strTop}{os.sep}{strNext}'
        if S_ISDIR(os.stat(strNextSearchIn, follow_symlinks = True).st_mode): # is a directory
            RecursiveFileSearch(strNextSearchIn)
        else: # is a file
            print(f'{strNextSearchIn} >>> ', end = '')
            for dictZ in WorkWithFile(strNextSearchIn).items():
                strStatus = 'OK' if dictZ[1] else 'ERRORS!'
                print(f'[{dictZ[0].upper()} : {strStatus}]', end = ' ')
            print()

### begin ###

if len(sys.argv) > 1:
    RecursiveFileSearch(sys.argv[1])
else:
    print('Syntax  : chk_ospf.py DIRECTORY')
    print('Example : chk_ospf.py /home/rancid/var/asr/configs')

###  end  ###




