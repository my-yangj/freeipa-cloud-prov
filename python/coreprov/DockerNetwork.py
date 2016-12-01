from .RemoteControl import RemoteControl

class DockerNetwork(RemoteControl):
    iptables_rules_path = "/var/lib/iptables/rules-save"

    def init_docker_network(self, host):
        ip = self.get_ip_addr(host)
        net = self.hconfig(host, 'network')
        if net.has_key('netif'):
            raise RuntimeError(
                "Not initializing host %s Docker net:  already exists" % host)
        print "Initializing Docker network on host %s (subnet %s)" % \
            (host, net['subnet'])
        netid = self.remote_run_output(
            "docker network create --subnet %(subnet)s --gateway %(gateway)s "
            "--ipam-opt=com.docker.network.bridge.enable_ip_masquerade=false "
            "%(name)s" % net, ip, quiet=False)
        net['netif'] = "br-%s" % str(netid[0][:12])
        self.pickle_config()  # stash netif for iptables, etc.

    def render_iptables_config(self, host):
        return self.render_jinja2(host, 'iptables-rules-save')

    def init_iptables(self, host):
        ip = self.get_ip_addr(host)
        print "Copying firewall rules to %s:%s" % (host, self.iptables_rules_path)
        self.put_file(
            ip, self.render_iptables_config(host), 'iptables-rules-save')
        self.remote_sudo(
            'mv iptables-rules-save %s' % self.iptables_rules_path, ip)
        self.remote_sudo(
            'systemctl restart iptables-restore.service', ip)