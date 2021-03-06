__metaclass__ = type

class FilterModule(object):
    ''' Query filter '''

    def formatmapstr(self, data, fmt, sep=''):
        items = [fmt.format(d) for d in data]
        return sep.join(items)

    def formatmaplist(self, data, fmt):
        items = [fmt.format(d) for d in data]
        return items

    def systemd_escape(self, data):
        """Convert a path into a string suitable for a systemd unit name,
        similar to the `systemd-escape(1)` command

        See https://www.freedesktop.org/software/systemd/man/systemd.unit.html
        """
        res = ''
        for i,c in enumerate(data):
            if i==0 and c=='/':
                # Throw away initial slashes
                continue
            elif (c=='.' and res==''):
                # Escape initial '.' C-style
                res += '\\x2e'
            elif (c>='a' and c<='z') or (c>='A' and c<='Z') \
                 or (c>='0' and c<='9') or (c=='_'):
                # Pass alphanumerics and underscore unchanged
                res += c
            elif c=='/':
                # Convert to dash
                res += '-'
            else:
                # Escape everything else C-style
                res += '\\' + hex(ord(c))[1:]
        return res

    def domain_to_dn(self, data):
        """Given a domain name, return the ldap DN,
        e.g. example.com|domain_to_dn returns dc=example,dc=com
        """
        return ','.join(map('dc={}'.format, data.split('.')))

    def ip_addr_list(self, host_list, hostvars):
        """Given a list of hosts and hostvars, return a list of IP
        addresses"""
        return [ hostvars[h]['ansible_default_ipv4']['address']
                 for h in host_list ]

    def filters(self):
        return {
            'formatmapstr': self.formatmapstr,
            'formatmaplist': self.formatmaplist,
            'systemd_escape': self.systemd_escape,
            'domain_to_dn': self.domain_to_dn,
            'ip_addr_list': self.ip_addr_list,
        }
