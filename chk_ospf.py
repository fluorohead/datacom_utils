import sys, os, re
from stat import S_ISDIR

def WorkWithFile(strFN):
    dictResult = {'ospf': True, 'ldp': True, 'mcast': True, 'pim': True}
    strPartEnding = '!\n'
    strStrip = 'interface '
    try:
        fileIn = open(strFN, mode = 'rt')
    except:
        print('Error opening!', file = sys.stderr)
        dictResult = {'ospf' : False, 'ldp' : False, 'mcast' : False, 'pim' : False}
    else:
        #print('Opening Ok')
        def FindPartition(strRegexp, strInterface, strExcludeInterface = ''):
            flagPresent = False
            listInterfaces = []
            for strLine2 in fileIn:
                if re.match(strRegexp, strLine2):
                    flagPresent = True
                    break
            if flagPresent:
                for strLine2 in fileIn:
                    if strLine2 != strPartEnding:
                        if re.match(strInterface, strLine2) and (not bool(re.match(strExcludeInterface, strLine2)) & bool(strExcludeInterface)):
                            listInterfaces.append(strLine2.strip().strip(strStrip))
                    else:
                        break
            else:
                fileIn.seek(0)
            return listInterfaces
        list_OSPFInterfaces = FindPartition('^router ospf \d{1,5}$\n', '^ {2}interface.*', '.*Loopback.*')
        if list_OSPFInterfaces:
            list_LDPInterfaces = FindPartition('^mpls ldp$', '^ {1}interface.*')
            list_MCASTInterfaces = FindPartition('^multicast-routing$', '^ {2}interface.*')
            list_PIMInterfaces = FindPartition('^router pim$', '^ {2}interface.*')
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
        fileIn.close()
    finally:
        return dictResult


def RecursiveFileSearch(strTop):
    for strNext in os.listdir(strTop):
        strNextSearchIn = f'{strTop}{os.sep}{strNext}'
        if S_ISDIR(os.stat(strNextSearchIn, follow_symlinks = False).st_mode): # is a directory
            RecursiveFileSearch(strNextSearchIn)
        else: # is a file
            print(f'{strNextSearchIn} >>> ', end = '')
            for dictZ in WorkWithFile(strNextSearchIn).items():
                strStatus = '\x1B[1;32;40mOK\x1B[0;;m' if dictZ[1] else '\x1B[1;31;40mERRORS!\x1B[0;;m'
                print(f'[{dictZ[0].upper()} : {strStatus}]', end = ' ')
            print()

### begin ###

if len(sys.argv) > 1:
    RecursiveFileSearch(sys.argv[1])
else:
    print('Syntax  : chk_ospf.py DIRECTORY')
    print('Example : chk_ospf.py /home/rancid/var/asr/configs')

###  end  ###




