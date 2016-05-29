# sensee
A complex sensor data server based on wsgiblank

## setup sensee
 - You need to have a user named as the application: ```useradd sensee```
 - When you are ready navigate to the root folder of the app and install it by: ```sudo make install```
 - Edit the corresponding sections of the configuration file ```sensee.conf```

### Apache setup
In order to make it work with Apache, you might need to add the following lines to its config (```/etc/apache2/apache2.conf```). However, before doing that you'd better create a backup of your current config. 

```
DocumentRoot /var/www/

WSGIScriptAlias /sensee /usr/lib/sensee/app/sensee.py

<Directory /usr/lib/sensee/app>
    Require all granted
    ErrorDocument 500 /sensee/errorlog
</Directory>
```
This way multiple different wsgi applications can be served through Apache, however, it is possible to have a single application in the root.
To have the module errorlog working with Apache's log, you must set the access permissions accordingly:

```
chmod 755 /var/log/apache2 
chmod 644 /var/log/apache2/error.log
```

And for the future rotation ```/etc/logrotate.d/apache2``` must be updated as well:

The line ```create 640 root adm``` should be replaced by ```create 644 root adm```.

## How to use sensee
You have two (three) options here:
 - Running sensee as a standalone python application (you might use a script ```sudo ./start.sh```)
 - Running from Apache (see the configuration above)
 - Never tried yet, but there is a DAEMON mode for mod_wsgi (yes I'm aware, that this is the recommended mode for running mod_wsgi)

## dependencies
- Python 2.7+
- Apache 2.4.10+
