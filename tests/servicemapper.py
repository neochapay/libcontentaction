#!/usr/bin/python3
import os
import dbus, dbus.service, dbus.mainloop.glib
from gi.repository import GObject as gobject

class ServiceMapper(dbus.service.Object):
    def __init__(self, path):
        dbus.service.Object.__init__(self, dbus.SessionBus(), path)
        self.iam = dbus.service.BusName('com.nokia.MServiceFw',
                                        dbus.SessionBus())
        self.mapping = {}
        try:
            exec(compile(open('service.map', "rb").read(), 'service.map', 'exec'))
        except IOError:
            exec(compile(open(os.path.dirname(__file__) + '/service.map', "rb").read(), os.path.dirname(__file__) + '/service.map', 'exec'))

    @dbus.service.method(dbus_interface='com.nokia.MServiceFwIf',
                         in_signature='s', out_signature='s')
    def serviceName(self, interface):
        return self.mapping.get(interface, '')

    @dbus.service.method(dbus_interface='org.maemo.contentaction.testing',
                         in_signature='ss', out_signature='')
    def changeMapping(self, implementor, interface):
        self.mapping[interface] = implementor

    @dbus.service.method(dbus_interface='org.maemo.contentaction.testing',
                         in_signature='ss', out_signature='')
    def emitServiceAvailable(self, implementor, interface):
        self.serviceAvailable(implementor, interface)

    @dbus.service.method(dbus_interface='org.maemo.contentaction.testing',
                         in_signature='s', out_signature='')
    def emitServiceUnavailable(self, implementor):
        self.serviceUnavailable(implementor)

    @dbus.service.signal(dbus_interface='com.nokia.MServiceFwIf',
                         signature='ss')
    def serviceAvailable(self, implementor, interface):
        print("emit service available", implementor, interface)

    @dbus.service.signal(dbus_interface='com.nokia.MServiceFwIf',
                         signature='s')
    def serviceUnavailable(self, implementor):
        print("emit service unavailable", implementor)

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
napper = ServiceMapper('/')
gobject.MainLoop().run()
