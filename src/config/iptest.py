# -*- encoding: utf-8 -*-

"""
平芜泫 DNS 代理服务器：IP 地址检测类。

is_ipv6 & v4tohex 的来源：https://gist.github.com/295930。
is_ipv4 作者：平芜泫（airyai@gmail.com）。
"""

def is_ipv4(ip):
	parts = ip.strip().split('.')
	if len(parts) != 4:
		return False
	for k in parts:
		try:
			v = int(k)
		except:
			return False
		if v < 0 or v > 255:
			return False
	return True

# converts a v4 ip to two v6 2-byte hex strings, unless one starts with '0'
# to cover that 'Not sure...' assert
def v4tohex(ip):
    v4 = ip.split('.')
    if not all(v4): return [ip]
    if len(v4) == 4:
        for p in v4:
            if int(p) > 255 or p[0] == '0': return [ip]
        n = ''.join(['%02X' % int(p) for p in v4])
        return [n[0:4],n[4:8]]
    else:
        return [ip]

def is_ipv6(ip):
    sip = ip.strip()
    # the general idea is convert '::' into '!!', then split on ':'
    # first, the '::' special case
    if sip == '::': sip = '!!'
    elif '!' in sip: return False
    # now edge cases
    if sip.startswith('::'):
        sip = sip.replace('::','!!:', 1)
    if sip.endswith('::'):
        sip = sip[::-1].replace('::', '!!:', 1)[::-1]
    # normal cases
    sip = sip.replace('::', ':!!:')
    # finally it's safe to split on ':'
    parts = sip.split(':')
    if not any(parts): return False
    # convert last part from v4 to v6, if possible
    if len(parts) > 1:
        p = parts.pop()
        parts.extend(v4tohex(p))
    # now expand our special '!!' to '0000' as much as needed, but no more
    nparts = []
    c = 0
    for i,p in enumerate(parts):
        if p == '!!':
            while len(nparts) < 9+i - len(parts):
                nparts.append('0000')
            c += 1
            if c > 1: return False
        else:
            nparts.append(p)
    parts = nparts
    # just sanity checks after this
    rparts = [p for p in parts if p]
    if not rparts: return False
    try:
        for p in rparts:
            assert len(p) <= 4
            int(p, 16)
        assert len(rparts) == 8
    except Exception, e:
        return False
    # one benefit is we'll return an 8 element list of more sane 2-byte hex strings (4 chars)
    # rather than whatever crazy crap was input
    return rparts

