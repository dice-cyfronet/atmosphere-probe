Usage of python-probe
=====================

* Install `python-simplejson`
* Copy scripts from `./python-probe/` to `/var/lib/nagios/nagios-probe/python-probe/`
* Chmod scripts to `nagios:nagios`
* Copy commands config from `./python-probe/air.cfg` to `/etc/nagios-plugins/config/air.cfg`
* Copy service config from `./python-probe/air_nagios2.cfg` to `/etc/nagios3/conf.d/air_nagios2.cfg`
* Fill `/var/lib/nagios/nagios-probe/python-probe/config.py.template` with proper `API_PRIVATE_TOKEN` and save as `/var/lib/nagios/nagios-probe/python-probe/config.py`
* Restart `nagios`