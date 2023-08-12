# SyndigoAssignment

Assignment Details:
    Create a Scrapy spider, that takes an arbitrary single product URL from www.target.com as command line argument,
    


Requirements:
  
    Ubuntu 22.04.3 LTS
    Python 3.10.12
    Virtual Enviornment
    Scrapy

Steps:

	1) Install Python
    	sudo apt-get install python

	2) create an Virtual Environment
    	sudo apt-get install python3-venv
    	python3 -m venv environmentName

	3) Install all the requirements in the environment
    	pip3 install -r requirements.txt

	5) Command for run the spider
    	scrapy crawl target -a url=...
        eg : scrapy crawl target -a url="https://www.target.com/p/baby-trend-expedition-race-tec-jogger-travel-system-8211-ultra-gray/-/A-79344798"
