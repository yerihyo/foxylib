import socket

import psutil
from foxylib.tools.collections.collections_tool import DictTool, merge_dicts


class PsutilTool:
    @classmethod
    def dict_inet2proto(cls):
        AF_INET6 = getattr(socket, 'AF_INET6', object())
        h = {
            (socket.AF_INET, socket.SOCK_STREAM): 'tcp',
            (AF_INET6, socket.SOCK_STREAM): 'tcp6',
            (socket.AF_INET, socket.SOCK_DGRAM): 'udp',
            (socket.AF_INET6, socket.SOCK_DGRAM): 'udp6',
        }
        return h

    @classmethod
    def connections_status(cls, tmplt=None):
        if tmplt is None:
            tmplt = "%-5s %-40s %-40s %-13s %-6s %s"

        l = [tmplt % (
            "Proto", "Local address", "Remote address", "Status", "PID",
            "Program name")]

        h_pid2name = merge_dicts([{p.info['pid']: p.info['name']}
                                  for p in psutil.process_iter(['pid','name'])],
                                 vwrite=DictTool.VWrite.no_duplicate_key)
        h_inet2proto = cls.dict_inet2proto()

        def connection2str(c):
            proto = h_inet2proto[(c.family, c.type)]
            laddr = "%s:%s" % c.laddr
            raddr = "%s:%s" % c.raddr if c.raddr else "-"
            status = c.status
            pid = c.pid or '-'
            pname = h_pid2name.get(c.pid, '?')[:15]
            return tmplt % (proto, laddr, raddr, status, pid, pname)

        prefix = "  "
        try:
            connections = psutil.net_connections(kind='inet')
            l.extend(map(connection2str, connections))

            return "\n".join(map(lambda s: f"{prefix}{s}", l))
        except psutil.AccessDenied:
            return f"{prefix}<AccessDenied>"
