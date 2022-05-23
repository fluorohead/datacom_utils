# version 1.0
import time, sys

listInbound = []
listOutbound = []
listSummarized = []

def OctetsAndMaskToDWORD_v4(strOneLine):
    listSplitted = strOneLine.split(sep = '.')
    if len(listSplitted) == 4:
        listLastOctetAndMask = listSplitted[-1].split(sep = '/')
        if (len(listLastOctetAndMask) == 2) and listLastOctetAndMask[0].isdigit() and listLastOctetAndMask[1].isdigit():
            listSplitted.pop(-1)
            listSplitted.append(listLastOctetAndMask[0])
            listSplitted.append(listLastOctetAndMask[1])
            if (int(listSplitted[-1]) <= 255) and listSplitted[0].isdigit() and listSplitted[1].isdigit() and listSplitted[2].isdigit() and listSplitted[3].isdigit():
                intOct1, intOct2, intOct3, intOct4, intMask = int(listSplitted[0]), int(listSplitted[1]), int(listSplitted[2]), int(listSplitted[3]), int(listSplitted[4])
                if (intOct1 | intOct2 | intOct3 | intOct4) <= 255:
                    intIP_DWORD = intOct4 | (intOct3 << 8) | (intOct2 << 16) | (intOct1 << 24)
                    intMASK_DWORD = ((2 ** intMask) - 1) << (32 - intMask)
                    intIP_DWORD = intIP_DWORD & intMASK_DWORD
                    intOct1 = (intIP_DWORD >> 24)
                    intOct2 = (intIP_DWORD >> 16) & 0xFF
                    intOct3 = (intIP_DWORD >> 8) & 0xFF
                    intOct4 = (intIP_DWORD) & 0xFF
                    intMaxIP = intIP_DWORD | (2 ** (32 - intMask) - 1)
                    listToAppend = [intOct1, intOct2, intOct3, intOct4, intMask, intIP_DWORD, intMASK_DWORD, intMaxIP]
                    listOutbound.append(listToAppend)
                    return True
    return False


def WordsAndMaskToLong_v6(strOneLine):
    strPermittedSymbols = '/0123456789:ABCDEFabcdef'
    flagWolfBillet = False
    for intK in range(0, len(strOneLine)):
        if not (strOneLine[intK] in strPermittedSymbols):
            flagWolfBillet = True
            break
    if (strOneLine.count('::') <= 1) and (not (':::' in strOneLine)) and (not flagWolfBillet):
        listSplitted = strOneLine.split(sep = ':')
        if ('/' in listSplitted[-1]) and ((listSplitted[0] != '') or strOneLine == '::/0'):
            list8WM = listSplitted[-1].split(sep = '/')
            if list8WM[-1] != '':
                listSplitted[-1] = list8WM[0]
                listSplitted.append(list8WM[1])
                if len(listSplitted) < 9: # ip net is not filled enough, lets fill it
                    intHowMuchToInsert = 0
                    intInsertIndex = 0
                    if listSplitted[-2] == listSplitted[-3] == '':
                        intHowMuchToInsert = 9 - len(listSplitted)
                        intInsertIndex = len(listSplitted) - 3
                    else:
                        try:
                            intInsertIndex = listSplitted.index('')
                        except Exception:
                            intHowMuchToInsert = 0
                            intInsertIndex = 0
                        else:
                            intHowMuchToInsert = 9 - len(listSplitted)
                    if not (intHowMuchToInsert == intInsertIndex == 0):
                        flagWolfBillet = False
                        while intHowMuchToInsert > 0:
                            listSplitted.insert(intInsertIndex, '')
                            intHowMuchToInsert -= 1
                    else:
                        flagWolfBillet = True
                if flagWolfBillet:
                    return False
                else:
                    listToAppend = []
                    for intZ in range(0, len(listSplitted) - 1):
                        if listSplitted[intZ] == '':
                            listToAppend.append(0)
                        else:
                            listToAppend.append(int(listSplitted[intZ], 16)) # words is hex in string
                            if listToAppend[-1] > 0xFFFF:
                                flagWolfBillet = True
                                break
                    if not flagWolfBillet:
                        # main process of conversion to LONG decimals
                        listToAppend.append(int(listSplitted[-1]))  # mask is decimal in string
                        if listToAppend[-1] <= 128:
                            intIPV6_LONG = 0x00000000000000000000000000000000
                            intIPV6_LONG = intIPV6_LONG | (listToAppend[0] << 112) | (listToAppend[1] << 96) | (listToAppend[2] << 80) | (listToAppend[3] << 64) | (listToAppend[4] << 48) | (listToAppend[5] << 32) | (listToAppend[6] << 16) | listToAppend[7]
                            intIPV6_BitMask = 0x00000000000000000000000000000000
                            intIPV6_BitMask = intIPV6_BitMask + ((2 ** (listToAppend[8]) - 1) << (128 - listToAppend[8]))
                            intIPV6_LONG = intIPV6_LONG & intIPV6_BitMask
                            listToAppend.append(intIPV6_LONG)
                            listToAppend.append(intIPV6_BitMask)
                            intIPV6_Max = 0x00000000000000000000000000000000
                            intIPV6_Max = intIPV6_LONG | (2 ** (128 - listToAppend[8]) - 1)
                            listToAppend.append(intIPV6_Max)
                            listOutbound.append(listToAppend)
                            return True
    return False


def TruncateOutboundLinesToPreserveMemory():
    for intK in range(0, len(listOutbound)):
        listOutbound[intK] = listOutbound[intK][8:12]


def UnZip128ToIPV6(intCur):
    listH = [hex(intCur >> 112)[2:], hex((intCur >> 96) & 0xFFFF)[2:], hex((intCur >> 80) & 0xFFFF)[2:], hex((intCur >> 64) & 0xFFFF)[2:], hex((intCur >> 48) & 0xFFFF)[2:], hex((intCur >> 32) & 0xFFFF)[2:], hex((intCur >> 16) & 0xFFFF)[2:], hex((intCur >> 0) & 0xFFFF)[2:]]
    listZ = []
    intZ = 0
    listGrp = [[0, 0], [0, 0], [0, 0]]  # one line = [counter, offset]
    for intZ in range(0, len(listH)):
        if listH[intZ] == '0':
            listZ.append(intZ)
    intGrp = 0
    flagGoOn = True
    intGrpOffset = 0
    intZ = 0
    # finding lenght of each repeated zeroes group and offset of such group
    while flagGoOn:
        if intZ < (len(listZ) - 1):
            if (listZ[intZ + 1] - listZ[intZ]) == 1:
                if listGrp[intGrp][0] == 0:
                    listGrp[intGrp][0] = 2
                    intGrpOffset = listZ[intZ]
                    listGrp[intGrp][1] = intGrpOffset
                else:
                    listGrp[intGrp][0] += 1
            else:
                listGrp[intGrp][1] = intGrpOffset
                intGrp += 1
            intZ += 1
        else:
            flagGoOn = False
    intMostLongIndex = -1
    intMostLongLength = -1
    # finding the most long group
    for intZ in range(0, 3):
        if listGrp[intZ][0] > 0:
            if listGrp[intZ][0] > intMostLongLength:
                intMostLongLength = listGrp[intZ][0]
                intMostLongIndex = intZ
    strOut = ''
    if intMostLongLength >= 0:
        intZ = 0
        listBefore = listH[0:(listGrp[intMostLongIndex][1])]
        listAfter = listH[(listGrp[intMostLongIndex][1] + listGrp[intMostLongIndex][0]):]
        strOut = ':'.join(listBefore) + '::' + ':'.join(listAfter)
    else:
        strOut = ':'.join(listH)
    return strOut


def SummarizePhase01_v4():
    while listOutbound != []:
        listToDelete = []
        intBegunok = 1
        while intBegunok < len(listOutbound):
            if (listOutbound[intBegunok][5] >= listOutbound[0][5]) and (listOutbound[intBegunok][7] <= listOutbound[0][7]):
                listToDelete.append(listOutbound[intBegunok])
                intBegunok += 1
            else:
                intBegunok = len(listOutbound) # stop inner 'while'
        listSummarized.append(listOutbound[0])
        listOutbound.pop(0)
        for listP in listToDelete:
            listOutbound.remove(listP)


def SummarizePhase01_v6():
    while listOutbound != []:
        listToDelete = []
        intBegunok = 1
        while intBegunok < len(listOutbound):
            if (listOutbound[intBegunok][1] >= listOutbound[0][1]) and (listOutbound[intBegunok][3] <= listOutbound[0][3]):
                listToDelete.append(listOutbound[intBegunok])
                intBegunok += 1
            else:
                intBegunok = len(listOutbound)  # stop inner 'while'
        listSummarized.append(listOutbound[0])
        listOutbound.pop(0)
        for listP in listToDelete:
            listOutbound.remove(listP)


def SummarizePhase02_v4():
    while listOutbound != []:
        listToDelete = []
        listReducedMask = listOutbound[0].copy()
        if listReducedMask[4] != 0:
            listReducedMask[4] -= 1 # /int mask
        listReducedMask[6]  = ((2 ** listReducedMask[4]) - 1) << (32 - listReducedMask[4]) # new DWORD bit mask
        listReducedMask[5] = listReducedMask[5] & listReducedMask[6] # new DWORD ip net
        listReducedMask[7] = listReducedMask[5] | (2 ** (32 - listReducedMask[4]) - 1) # new DWORD max ip
        intBegunok = 1
        if listReducedMask[5] != listOutbound[0][5]: # not the same ip net beginning
            listSummarized.append(listOutbound[0])
            listOutbound.pop(0)
        else:
            while intBegunok < len(listOutbound):
                if listReducedMask[4] == 0:
                    intBegunok = len(listOutbound) # stop inner 'while'
                    listSummarized.append(listOutbound[0])
                    listOutbound.pop(0)
                else:
                    if (listOutbound[intBegunok][5] >= listOutbound[0][5]) and (listOutbound[intBegunok][7] == listReducedMask[7]):
                        listToDelete.append(listOutbound[intBegunok])
                        intBegunok += 1
                    else:
                        intBegunok = len(listOutbound) # stop inner 'while'
            if listToDelete != [] :
                listReducedMask[0] = (listReducedMask[5] >> 24)  # new octet 1
                listReducedMask[1] = (listReducedMask[5] >> 16) & 0xFF  # new octet 2
                listReducedMask[2] = (listReducedMask[5] >> 8) & 0xFF  # new octet 3
                listReducedMask[3] = (listReducedMask[5]) & 0xFF  # new octet 4
                listSummarized.append(listReducedMask)
            else:
                listSummarized.append(listOutbound[0])
            listOutbound.pop(0)
            for listD in listToDelete:
                listOutbound.remove(listD)


def SummarizePhase02_v6():
    while listOutbound != []:
        listToDelete = []
        listReducedMask = listOutbound[0].copy()
        if listReducedMask[0] != 0: # /int mask
            listReducedMask[0] -= 1
        listReducedMask[2] = ((2 ** listReducedMask[0]) - 1) << (128 - listReducedMask[0])  # new 128 bit mask
        listReducedMask[1] = listReducedMask[1] & listReducedMask[2] # new 128 bit net
        listReducedMask[3] = listReducedMask[1] | (2 ** (128 - listReducedMask[0]) - 1) # new 128 bit Max IP
        intBegunok = 1
        if listReducedMask[1] != listOutbound[0][1]: # not the same ip net beginning
            listSummarized.append(listOutbound[0])
            listOutbound.pop(0)
        else:
            while intBegunok < len(listOutbound):
                if listReducedMask[0] == 0:
                    intBegunok = len(listOutbound)  # stop inner 'while'
                    listSummarized.append(listOutbound[0])
                    listOutbound.pop(0)
                else:
                    if (listOutbound[intBegunok][1] >= listOutbound[0][1]) and (listOutbound[intBegunok][3] == listReducedMask[3]):
                        listToDelete.append(listOutbound[intBegunok])
                        intBegunok += 1
                    else:
                        intBegunok = len(listOutbound)  # stop inner 'while'
            if listToDelete != []:
                listSummarized.append(listReducedMask)
            else:
                listSummarized.append(listOutbound[0])
            listOutbound.pop(0)
            for listD in listToDelete:
                listOutbound.remove(listD)


######### begin ##############

if (len(sys.argv) == 3) and (sys.argv[1] in ['-4','-6']):
    intAF = ord(sys.argv[1][1])
    strDone = 'Done!'

    try:
        fileInput = open(sys.argv[2], mode = 'rt')
    except:
        print('Error opening file.')
    else:
        for strLine in fileInput:
            listInbound.append(strLine.strip())

        print(f'Checking for correct IPv{chr(intAF)} addresses...', end = '')

        if intAF == 52: # char '4'
            for strLine in listInbound: OctetsAndMaskToDWORD_v4(strLine)
        else:
            for strLine in listInbound: WordsAndMaskToLong_v6(strLine)

        print(strDone)

        intNS_start = time.perf_counter_ns()
        intInboundSize = len(listInbound)
        listInbound = []
        fileInput.close()

        if listOutbound != []:
            print('Sorting....', end = '')
            listOutbound.sort()
            print(strDone)
            print('Summarizing...', end = '')
            if intAF == 52: # char '4'
                SummarizePhase01_v4()
            else:
                TruncateOutboundLinesToPreserveMemory() # outbound now = [[mask_len, 128bit_net, 128bit_mask, 128bit_max_ip]]
                SummarizePhase01_v6()
            intOutboundSize = 0
            if intAF == 52: # char '4'
                while intOutboundSize != len(listSummarized):
                    listOutbound = listSummarized.copy()
                    intOutboundSize = len(listOutbound)
                    listSummarized = []
                    SummarizePhase02_v4()
            else:
                while intOutboundSize != len(listSummarized):
                    listOutbound = listSummarized.copy()
                    intOutboundSize = len(listOutbound)
                    listSummarized = []
                    SummarizePhase02_v6()
            print(strDone)
            print(f'Prefixes before : {intInboundSize}')
            print(f'Prefixes after  : {len(listSummarized)}')
            listDelta = [0, 0, 0, 0, 0, 0]
            listValues = ['hrs', 'min', 'sec', 'millisec', 'microsec', 'nanosec']
            intNS_delta = time.perf_counter_ns() - intNS_start
            intNS_delta_seconds = intNS_delta // (10 ** 9)
            listDelta[0] = intNS_delta_seconds // 3600
            listDelta[1] = (intNS_delta_seconds - listDelta[0] * 3600) // 60
            listDelta[2] = intNS_delta_seconds - listDelta[0] * 3600 - listDelta[1] * 60
            listDelta[3] = (intNS_delta - (10 ** 9) * (listDelta[0] * 3600 + listDelta[1] * 60 + listDelta[2])) // (10 ** 6)
            listDelta[4] = (intNS_delta - listDelta[3] * (10 ** 6) - (10 ** 9) * (listDelta[0] * 3600 + listDelta[1] * 60 + (listDelta[2]))) // (10 ** 3)
            listDelta[5] = intNS_delta - listDelta[3] * (10 ** 6) - listDelta[4] * (10 ** 3) - (10 ** 9) * (listDelta[0] * 3600 + listDelta[1] * 60 + listDelta[2])
            strTimeResult = 'Processing time : '
            for intI in range(0, len(listDelta)):
                if listDelta[intI] != 0:
                    strTimeResult += f'{listDelta[intI]} {listValues[intI]}, '
            strTimeResult = strTimeResult[0:-2] + '.'
            print(strTimeResult)
            print('Writing to file...', end = '')
            time.sleep(1)
            strFileName = time.strftime('netsum-%Y-%m-%d-%H-%M-%S.txt')
            try:
                fileOutput = open(strFileName, mode = 'wt')
            except:
                print('Error creating file.')
            else:
                if intAF == 52: # char '4'
                    for listK in listSummarized:
                        fileOutput.write(f'{listK[0]}.{listK[1]}.{listK[2]}.{listK[3]}/{listK[4]}\n')
                else:
                    for listK in listSummarized:
                        fileOutput.write(f'{UnZip128ToIPV6(listK[1])}/{listK[0]}\n')
                fileOutput.flush()
                fileOutput.close()
                print(strDone)
                print(f'Your file is : {strFileName}')
        else:
            print('Nothing to do.')
else:
    print('Syntax : netsum.py OPTION FILENAME')
    print('Option : \'-4\' for ipv4 address family, \'-6\' for ipv6 address family')
    print('Example : netsum.py -4 fullview.txt')

######### end ##############
