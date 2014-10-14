import os
import air.config

pwd = os.path.dirname(os.path.abspath(__file__))
air.config.add_config_ini('%s/main.ini' % pwd, '%s/secure.ini' % pwd)

from air.mapping import port_mappings

__author__ = 'paoolo'

if __name__ == '__main__':
    mappings = port_mappings.get_all_port_mappings(_all=True)

    if 'port_mappings' in mappings:
        mappings = mappings['port_mappings']
        mappings = sorted(mappings, key=lambda element: element['source_port'])
        for mapping in mappings:
            print '%d; %s' % (int(mapping['source_port']), str(mapping))
        for mapping in mappings:
            print int(mapping['source_port'])