#!/usr/bin/env bash
#scp bin/LaserBoth.hex pi@192.168.0.123:both.hex
scp bin/LaserStart.hex pi@192.168.0.123:start.hex

ssh pi@192.168.0.123 './flash.sh t45 start.hex '
