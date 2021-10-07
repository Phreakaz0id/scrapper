ENV = .env

export GREEN=\033[0;32m
export NOFORMAT=\033[0m

default: help

#❓ help: @ Displays this message
help:
	@echo ""
	@echo "List of available MAKE targets for development usage."
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Examples:"
	@echo ""
	@echo "	make ${GREEN}scrap.maxiconsumo.limpieza${NOFORMAT}	- Scraps limpieza category from maxiconsumo website"
	@echo "	make ${GREEN}scrap.maxiconsumo.perfumeria${NOFORMAT}	- Scraps perfumeria category from maxiconsumo website"
	@echo ""
	@grep -E '[a-zA-Z\.\-]+:.*?@ .*$$' $(MAKEFILE_LIST)| tr -d '#'  | awk 'BEGIN {FS = ":.*?@ "}; {printf "${GREEN}%-30s${NOFORMAT} %s\n", $$1, $$2}'

#🗑  clear.logs: @  Clears all logs
clear.logs: SHELL:=/bin/bash
clear.logs:
	rm logs/*

#🕷  main: @  Runs the main program using the environment settings
main: SHELL:=/bin/bash
main:
	@source ${ENV} && python main.py

#🕷  scrap.maxiconsumo.limpieza: @  Scraps limpieza category from maxiconsumo website
scrap.maxiconsumo.limpieza: SHELL:=/bin/bash
scrap.maxiconsumo.limpieza:
	@source ${ENV} ENV && scrapy crawl maxiconsumo -s LOG_ENABLED=0 -o maxiconsumo_limpieza.csv -a category="limpieza" -a max_pages=14

#🕷  scrap.maxiconsumo.perfumeria: @ Scraps perfumeria category from maxiconsumo website
scrap.maxiconsumo.perfumeria: SHELL:=/bin/bash
scrap.maxiconsumo.perfumeria:
	@source ${ENV} ENV && scrapy crawl maxiconsumo -s LOG_ENABLED=0 -o maxiconsumo_perfumeria.csv -a category="perfumeria" -a max_pages=18

#🕷  scrap.yaguar.limpieza: @  Scraps limpieza category from yaguar website
scrap.yaguar.limpieza: SHELL:=/bin/bash
scrap.yaguar.limpieza:
	@source ${ENV} ENV && scrapy crawl yaguar -s LOG_ENABLED=1 -o yaguar_limpieza.csv -a category="limpieza"

#🕷  scrap.yaguar.perfumeria: @  Scraps perfumeria category from yaguar website
scrap.yaguar.perfumeria: SHELL:=/bin/bash
scrap.yaguar.perfumeria:
	@source ${ENV} ENV && scrapy crawl yaguar -s LOG_ENABLED=1 -o yaguar_perfumeria.csv -a category="perfumeria"

#📦 setup: @ Installs dependencies
setup:
	@pip install -r requirements.txt
