from pritunl.host.host import Host

from pritunl.constants import *
from pritunl.exceptions import *
from pritunl.helpers import *
from pritunl import settings
from pritunl import event
from pritunl import utils

import datetime

def get_host(id):
    return Host(id=id)

def iter_hosts(spec=None, fields=None):
    spec = spec or {}

    if fields:
        fields = {key: True for key in fields}

    for doc in Host.collection.find(spec, fields).sort('name'):
        yield Host(doc=doc)

def init_host():
    settings.local.host = Host()

    try:
        settings.local.host.load()
    except NotFound:
        pass

    settings.local.host.status = ONLINE
    settings.local.host.users_online = 0
    settings.local.host.start_timestamp = utils.now()
    if settings.local.public_ip:
        settings.local.host.auto_public_address = settings.local.public_ip

    settings.local.host.commit()
    event.Event(type=HOSTS_UPDATED)

def deinit_host():
    Host.collection.update({
        '_id': settings.local.host.id,
    }, {'$set': {
        'status': OFFLINE,
        'ping_timestamp': None,
    }})
    event.Event(type=HOSTS_UPDATED)
