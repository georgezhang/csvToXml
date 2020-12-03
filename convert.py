#! usr/bin/python

import csv
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom

CONF = {'version': '0.7.1.136', 'savepassword': 'True'}
ROOT = {'type': 'database', 'name': 'COMPANY', 'expanded': 'True'}


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-16')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='  ')


def buildRouter(parentElement, host, ip):
    connection = SubElement(parentElement, 'connection', {'type': 'PuTTY', 'name': host})
    connection_info = SubElement(connection, 'connection_info')

    name = Element('name')
    name.text = host
    protocol = Element('protocol')
    protocol.text = 'SSH'
    host = Element('host')
    host.text = ip
    port = Element('port')
    port.text = '22'
    description = Element('description')
    connection_info.extend([name, protocol, host, port, description])

    command = SubElement(connection, 'command')
    command1 = Element('command1')
    command2 = Element('command2')
    command.extend([command1, command2])


"""
  BUILD YOUR XML HERE
"""


def main():
    configuration = Element('configuration', CONF)
    root = SubElement(configuration, 'root', ROOT)

    with open('DeviceList.csv', 'rt') as f, open('DeviceList.xml', 'w') as o:
        reader = csv.reader(f)
        next(reader, None)  # skip the headers
        for row in reader:
            Host, IP = row
            buildRouter(root, Host, IP)

        output = prettify(configuration)
        print(output)
        o.write(output)


if __name__ == '__main__':
    main()
