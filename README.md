# datacom_utils
netsum.py is a Python3 script utility for summarizing ipv4 and ipv6 net lists.
Script gets input file with a list of networks and tries to find and pop superceded networks from list if there's superior net.
At the second phase script tries to reduce mask length (24 -> 23 for e.g.) and finds superceded nets again. Then the algorithm works again
and again, until length of input list equals length of output list.
