#!/bin/bash

echo " --> chmod 775 "/usr/local/nagios/share/perfdata" "/usr/local/nagiosxi/html/includes/components/capacityplanning/backend/capacityplanning.py" "/usr/local/nagiosxi/var/components/capacityplanning.log""

chmod 775 "/usr/local/nagios/share/perfdata" "/usr/local/nagiosxi/html/includes/components/capacityplanning/backend/capacityplanning.py" "/usr/local/nagiosxi/var/components/capacityplanning.log"

echo " --> find / -d -iname "cpmetrix" 2>/dev/null|xargs chmod -R 775"
find / -d -iname "cpmetrix" 2>/dev/null|xargs chmod -R 775

echo " --> find / -d -iname "cpmetrix" 2>/dev/null|xargs chown nagios.nagios -R"
find / -d -iname "cpmetrix" 2>/dev/null|xargs chown nagios.nagios -R
