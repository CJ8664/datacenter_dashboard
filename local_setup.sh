#!/bin/zsh
curl -X POST -H 'Content-Type: application/json' -d @log_spec.json http://35.231.108.142:8090/druid/indexer/v1/supervisor
curl -X POST -H 'Content-Type: application/json' -d @metrics_spec.json http://35.231.108.142:8090/druid/indexer/v1/supervisor
