from air import port_mapping_templates, appliance_sets, appliances, dev_mode_property_sets

__author__ = 'paoolo'

if __name__ == '__main__':
    _app_set = appliance_sets.create_app_set(
        appliance_set_type=appliance_sets.APP_SET_TYPE_DEV)
    print _app_set
    print '----'

    _app = appliances.create_app(_app_set['appliance_set']['id'], 1)
    print _app
    print '----'

    _dev_sets = dev_mode_property_sets.get_all_dev_mode_property_set()
    print _dev_sets
    print '----'

    _dev_id = port_mapping_templates.get_dev_id_for_app(_app['appliance']['id'], _dev_sets)
    print _dev_id
    print '----'

    try:
        print port_mapping_templates.get_all_port_map_temp_by_dev(_dev_id['id'])
        print '----'

        _port_mapping = port_mapping_templates.create_port_map_temp_for_dev(_dev_id['id'], 'tcp', 'none', 'telnet', 25)
        print _port_mapping
        print '----'

        print port_mapping_templates.get_all_port_map_temp_by_dev(_dev_id['id'])
        print '----'

        print port_mapping_templates.update_port_map_temp(_port_mapping['port_mapping_template']['id'],
                                                          service_name='http', target_port=80)
        print '----'

        print port_mapping_templates.get_all_port_map_temp_by_dev(_dev_id['id'])
        print '----'

        print port_mapping_templates.delete_port_map_temp(_port_mapping['port_mapping_template']['id'])
        print '----'

    finally:
        print appliances.delete_app(_app['appliance']['id'])
        print appliance_sets.delete_app_set(_app_set['appliance_set']['id'])
