import socket
import threading
import socketserver
import Constants

class Message():
    
    def __init__(self, msg_type):
        self.msg_type = msg_type

    def payload(self):
        return None

    def get_string(self):
        s = "{}".format(self.msg_type)
        p = payload()
        if p != None:
            s += Constants.THIP_SEPARATOR + p
        return s

    def get_packet(self)
        return bytes(self.get_string(), "utf-8")


class RequestServiceNameMessage(Message):
    
    def __init__(self):
        Message.__init__(Constants.THIP_REQUEST_SERVICE_NAME)


class NotifyServiceNameMessage(Message):
    
    def __init__(self, name):
        Message.__init__(Constants.THIP_NOTIFY_SERVICE_NAME)
        self.name = name

    def payload(self):
        return name


def message_from_string(msg_str):
    s = msg_str.split(Constants.THIP_SEPARATOR)
    msg_type, payload = int(s[0]), None
    if len(s) > 1:
        payload = s[1]

    #according to message type
    if msg_type == Constants.THIP_REQUEST_SERVICE_NAME:
        return RequestServiceNameMessage()
    if msg_type == Constants.THIP_NOTIFY_SERVICE_NAME:
        return NotifyServiceNameMessage(payload)

    return None


def message_from_packet(packet):
    return message_from_string(str(packet, "utf-8"))
    

class ThIPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.server.handle_datagram_request(self.request[0].strip(), self.request[1], self.client_address)


class ThIPServer(socketserver.UPDServer):

    def __init__(self, service, host, port):
        socketserver.UPDServer.__init__(self, (host, port), ThIPHandler)
        self.service = service

    def handle_datagram_request(self, data, socket, client):
        msg = message_from_string(data)
        if msg.msg_type == Constants.THIP_REQUEST_SERVICE_NAME:
            resp = NotifyServiceNameMessage(self.service.name)
            socket.sendto(resp.get_string(), client)


class Service:

    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port


class LocalService(Service):

    def __init__(self, name = Constants.DEFAULT_SERVICE_NAME, port = Constants.DEFAULT_SERVICE_PORT):
        Service.__init__(self, name, "localhost", port)
        self.server = ThIPServer(self, self.host, self.port)

    def start():


class RemoteService(Service):

    def __init__(self, host = "localhost", port = Constants.DEFAULT_SERVICE_PORT):
        Service.__init__(self, Constants.DEFAULT_SERVICE_NAME, host, port)