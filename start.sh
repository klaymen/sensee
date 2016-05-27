service apache2 stop
make uninstall
make install
service apache2 start
su -c "python /usr/lib/sensee/app/sensee.py" sensee
