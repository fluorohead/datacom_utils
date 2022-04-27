import paramiko, socket, sys

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh_client.connect(sys.argv[1], username = '', password = '', timeout = 5)
except TimeoutError:
    print('TimeoutError.')
except socket.gaierror:
    print('socket.gaierror.')
except paramiko.ssh_exception.AuthenticationException:
    print('paramiko.ssh_exception.AuthenticationException.')
except:
    print('Unknown error.')
else:
    ssh_chan = ssh_client.invoke_shell(term = 'vt100', width = 200, height = 24, width_pixels = 0, height_pixels = 0, environment = None)
    ssh_chan.settimeout(5)

    def SendAndReceive_HuaweiNE40(strCommand = b'', strPager = b'', strPrompt = b'', strQuitOrMore = b' '):
        strResult = b''
        strRec = b''
        if strCommand :
            ssh_chan.send(strCommand)
        while True:
            try:
                strRec = ssh_chan.recv(10000)
                #print(f'one line recv {strRec}')
            except:
                #print(b' Exception after line ---> ' + strRec)
                # сюда попадаем только когда не знаем какой у нас промпт или забыли \n в конце команды
                strRec = None
                break
            else:
                if strRec.strip().endswith(strPager) and strPager:
                    #print('Ends with pager line! Sending space.')
                    strRec = None
                    ssh_chan.send(strQuitOrMore)
                else:
                    if strRec.strip().endswith(strPrompt) and strPrompt:
                        #print('Ends with prompt!')
                        strRec = None
                        break
            finally:
                if not (strRec == None):
                    strResult += strRec
                else:
                    strResult = strResult.rstrip(strPager)
        if strResult :
            strResult = strResult.replace(b'\x1b[42D                                          \x1b[42D', b'')
        return strResult

    strPrefCmd = b'disp nat session table source-vpn-instance '
    list_NAT_Sessions = [[strPrefCmd + b'RFC-NAT-PLUS slot 4 card 0\n', 'RFC-NAT', b'0', 0],
                         [strPrefCmd + b'M-UPRAVA-NAT-INS slot 4 engine 0\n', 'M-UPRAVA-NAT', b'0', 3020],
                         [strPrefCmd + b'DNO-INS slot 5 engine 0\n', 'DNO1', b'0', 3030],
                         [strPrefCmd + b'DNO-INS slot 5 engine 1\n', 'DNO2', b'0', 3030],
                         [strPrefCmd + b'DEMO-INS slot 5 card 0\n', 'DEMO', b'0', 3040],
                         [strPrefCmd + b'M-UPRAVA-INET-INS slot 4 card 0\n','M-UPRAVA-INET', b'0', 3045],
                         [strPrefCmd + b'DNO-DETI-INV-INS slot 5 card 0\n', 'DNO-DETI-INV', b'0', 3050],
                         [strPrefCmd + b'MGTS-WIFI-HEXNAT-INS slot 5 card 0\n', 'MGTS-WIFI-HEXNAT', b'0', 3065],
                         [strPrefCmd + b'DPI-MGTS-INS slot 5 card 0\n', 'RODCONTROL', b'0', 3070],
                         [strPrefCmd + b'WIFI-HP-NAT-DPI-INS slot 5 card 0\n', 'WIFI-HP-NAT-DPI', b'0', 3085],
                         [strPrefCmd + b'DEPCULT-INS slot 5 card 0\n', 'DEPCULT', b'0', 3090]]
    k = b''
    strPrm = b''
    strCTS = b'Current total sessions: '

    #for k in SendAndReceive_HuaweiNE40().split(b'\r\n'): print(k)
    strPrm = SendAndReceive_HuaweiNE40().split(b'\r\n')[-1] # last k is prompt
    #print(f'The prompt is : {strPrm}')

    intZ = 0
    for listCmd in list_NAT_Sessions:
        for k in SendAndReceive_HuaweiNE40(listCmd[0], b'---- More ----', strPrm, b'q').split(b'\r\n'):
            #print(k)
            intOffset = k.find(strCTS)
            if not intOffset:
                #print(f'string {strCTS} is found!')
                list_NAT_Sessions[intZ][2] = k[len(strCTS):-1]
                break
        intZ += 1

    for l in list_NAT_Sessions: print('%s:%s ' % (l[1], l[2].decode('latin-1')), end = '')

    #print('>>> Real End.')
    ssh_client.close()