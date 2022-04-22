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
        list_LDPInterfaces = []
        list_MCASTInterfaces = []
        list_PIMInterfaces = []
        for strLine in fileIn: # searching for router ospf 1 beginning
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
            flagLDP_Present = False
            flagMCAST_Present = False
            flagPIM_Present = False
            for strLine in fileIn: #searching for mpls ldp beginning
                if re.match('^mpls ldp$\n', strLine):
                    #print('mpls ldp pattern found')
                    flagLDP_Present = True
                    break
            if flagLDP_Present:
                for strLine in fileIn: # searching for mpls ldp ending
                    if strLine != strPartEnding:
    #                    print(strLine, end='')
                        if re.match('^ interface.*', strLine):
                            list_LDPInterfaces.append(strLine.strip().strip(strStrip))
                    else:
                        break
                #print(f'LDP : {list_LDPInterfaces}')
            else:
                #print('No MPLS LDP partition found')
                fileIn.seek(0)
            for strLine in fileIn: #searching for multicast-routing beginning
                if re.match('^multicast-routing.*', strLine):
                    #print('multicast-routing partition found')
                    flagMCAST_Present = True
                    break
            if flagMCAST_Present:
                for strLine in fileIn: #searching for multicast-routing ending
                    if strLine != strPartEnding:
                        if re.match('^ {2}interface.*', strLine):
                            list_MCASTInterfaces.append(strLine.strip().strip(strStrip))
                    else:
                        break
                #print(f'MCAST : {list_MCASTInterfaces}')
            else:
                #print('No multicast-routing partition found')
                fileIn.seek(0)
            for strLine in fileIn: #searching for router pim beginning
                if re.match('^router pim.*', strLine):
                    #print('router pim partition found')
                    flagPIM_Present = True
                    break
            if flagPIM_Present:
                for strLine in fileIn: #searching for router pim ending
                    if strLine != strPartEnding:
                        if re.match('^ {2}interface.*', strLine):
                            list_PIMInterfaces.append(strLine.strip().strip(strStrip))
                    else:
                        break
                #print(f'PIM : {list_PIMInterfaces}')
            else:
                #print('No router pim partition found')
                fileIn.seek(0)
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




