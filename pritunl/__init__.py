__title__ = 'pritunl'
__version__ = '0.0.0'
__author__ = 'Zachary Huff'
__license__ = 'AGPL'
__copyright__ = 'Copyright 2013 Zachary Huff'
import threading

openssl_lock = threading.Lock()

from wsgi_server import WsgiServer
server = WsgiServer()
