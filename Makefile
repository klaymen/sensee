PWD=`pwd`
DESTINATION=$(install_root)/usr/lib

USER=sensee
GROUP=sensee

CP=cp
LCP=ln -s
CONF_DIR=/etc/sensee
CACHE_DIR=/var/cache/sensee
LOG_DIR=/var/log/sensee
WWW=/var/www/html
CONFS=sensee.conf users

all:
	@echo "Type 'make install' to install package"

uninstall:
	rm -rf $(DESTINATION)/sensee
	find $(WWW)/ -type d -name 'sensee_*' | xargs rm -r
	rm -rf $(CONF_DIR)
	rm -rf $(LOG_DIR)
	rm -rf $(CACHE_DIR)

install:
	mkdir -p $(DESTINATION)/sensee
	cp ./* -r $(DESTINATION)/sensee
	mv $(DESTINATION)/sensee/static/sensee_*/ $(WWW)
	mkdir -p $(CONF_DIR)
	mkdir -p $(CACHE_DIR)
	chown -R $(USER):$(GROUP) $(CACHE_DIR)
	mkdir -p $(LOG_DIR)
	chown -R $(USER):$(GROUP) $(LOG_DIR)
	@for n in $(CONFS) ; do rm -f $(CONF_DIR)/$$n ; echo $$n ; $(CP) $(PWD)/$$n $(CONF_DIR)/$$n; done
	@for n in $(WWW)/sensee_*/ ; do printf "Create symlink for "; ln -sf $$n $(DESTINATION)/sensee/static | basename $$n ; done
