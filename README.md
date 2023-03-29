# datacom_utils
<b>netsum.py</b>
Script for summarizing ipv4 and ipv6 net lists.
Script gets input file with a list of networks and tries to find and to pop superceded networks if there's superior net.
At second phase script tries to reduce mask length (/24 -> /23 for e.g.) and finds superceded nets again. Then the algorithm works again
and again, reducing the mask more and more, until length of input list equals length of output list - is the stop condition.

<b>chk_ospf.py</b>
Script for processing Rancid config files of Cisco routers, working on IOS XR operational system.
It checks the interfaces under 'router ospf' partition are also present in another partitions, like 'mpls ldp', 'multicast-routing' and 'router pim'.
It is usefull for MPLS routers with multicast-routing enabled in GRT.
