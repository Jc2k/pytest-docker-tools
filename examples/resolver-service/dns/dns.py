#! /usr/bin/python

import fnmatch
import os

from dnslib import MX, PTR, RR, SOA, TXT, A
from dnslib.dns import QTYPE
from dnslib.server import BaseResolver, DNSLogger, DNSServer


class Logger(DNSLogger):

    def log_request(self, handler, request):
        print(request)

    def log_reply(self, handler, reply):
        print(reply)
        self.log_data(reply)


class Resolver(BaseResolver):

    def _resolve_request(self, request):
        name = str(request.q.qname).strip('.').replace('.', '_').upper()
        rec_type = QTYPE[request.q.qtype]
        environ_key = f'DNS_{name}__{rec_type}'

        for glob, value in os.environ.items():
            if not glob.startswith('DNS_'):
                continue

            if fnmatch.fnmatch(environ_key, glob):
                return value

    def resolve(self, request, handler):
        reply = request.reply()
        value = self._resolve_request(request)

        if value and request.q.qtype == QTYPE.MX:
            reply.add_answer(
                RR(request.q.qname, QTYPE.MX, rdata=MX(label=value)),
            )
        elif value and request.q.qtype == QTYPE.A:
            reply.add_answer(
                RR(request.q.qname, QTYPE.A, rdata=A(value)),
            )
        elif value and request.q.qtype == QTYPE.TXT:
            reply.add_answer(RR(
                request.q.qname,
                QTYPE.TXT,
                rdata=TXT(value),
            ))
        elif value and request.q.qtype == QTYPE.PTR:
            reply.add_answer(RR(
                request.q.qname,
                QTYPE.PTR,
                rdata=PTR(value),
            ))

        reply.add_auth(
            RR(request.q.qname, QTYPE.SOA, ttl=60, rdata=SOA(
                "ns1.local.dev", "ns2.local.dev",
                (20140101, 3600, 3600, 3600, 3600),
            ))
        )

        reply.add_ar(RR("ns1.local.dev", ttl=60, rdata=A("127.0.0.1")))

        return reply


if __name__ == '__main__':
    logger = Logger()

    server = DNSServer(
        Resolver(),
        port=53,
        address='0.0.0.0',
        logger=logger,
    )

    server.start()
