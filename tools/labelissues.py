#!/usr/bin/python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import time

from github3 import GitHub

# Add webcompat module to import path
sys.path.append(os.path.realpath(os.pardir))

from webcompat.form import domain_name
from webcompat.helpers import extract_url
from webcompat.db import Site
from webcompat.db import site_db


if __name__ == "__main__":
    gh = GitHub(token='35cecb11703f141d78439f6817cac08822627311')

    fp = open('web-bugs.txt', 'w')

    for i in range(7651, 7840):
        try:
            issue = gh.issue('webcompat', 'web-bugs', i)
            host_name = domain_name(extract_url(issue.body))
            print str(issue.number) + " " + host_name
            if host_name:
                found = False
                for site in site_db.query(Site).filter_by(url=host_name):
                    result = '{} {} {}'.format(issue.number, host_name,
                                               site.priority)
                    fp.write(result + '\n')
                    fp.flush()
                    found = True

                if not found:
                    subparts = host_name.split('.')
                    domains = ['.'.join(subparts[i:])
                               for i, subpart in enumerate(subparts)
                               if 0 < i < host_name.count('.')]
                    for domain in domains:
                        for site in site_db.query(Site).filter_by(url=domain):
                            result = '{} {} {}'.format(issue.number, domain,
                                                       site.priority)
                            fp.write(result + '\n')
                            fp.flush()

        except Exception, e:
            print str(e)
            pass

        if i % 100 == 0:
            time.sleep(30)
