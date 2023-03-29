# datacom_utils
<b>netsum.py</b>

Script for summarizing ipv4 and ipv6 nets.
Gets input file with a list of networks and tries to find and pop superceded networks if corresponding superior net are also present in the same list.
At second phase tries to reduce mask length (/24 -> /23 for e.g.) and finds superceded nets again. Then the algorithm works again
and again, reducing the mask more and more, until length of input list equals length of output list (reached stop condition).


<b>chk_ospf.py</b>

Script for processing Rancid files with Cisco IOS XR routers configurations.
Checks that interfaces under 'router ospf' partition are also present in another partitions, like 'mpls ldp', 'multicast-routing' and 'router pim'.
Usefull for MPLS routers with multicast-routing enabled in GRT.
