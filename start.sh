service apache2 stop
make uninstall
make install
service apache2 start
python /usr/lib/sensee/app/sensee.py
