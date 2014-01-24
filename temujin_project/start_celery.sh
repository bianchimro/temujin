#!/bin/bash

source ../env/bin/activate
celery -A temujin_project  worker -l info