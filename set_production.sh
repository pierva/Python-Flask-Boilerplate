#!/usr/bin/env bash

export APP_SETTINGS='application.config.ProductionConfig'


mkdir application/instance
touch application/instance/production.cfg
mkdir log
touch log/error.log
chgrp www-data log
chgrp www-data log/error.log
chmod 700 log
chmod 664 log/error.log
