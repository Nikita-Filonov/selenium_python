# Selenium python

(Demo allure report)[https://nikita-filonov.github.io/selenium_python/]

**Install project**

```
git clone https://github.com/Nikita-Filonov/selenium_python.git
cd selenium_python
```

**Setup env**

Make sure to create `.env` file locally. You can copy all content from `.env.example`

```
REMOTE_URL="http://selenium-hub:4444/wd/hub"
BASE_URL="https://www.w3schools.com"
SCREENSHOTS_ON=true
```

**Running locally**

If you want to run auto tests locally, make sure to install `python 3.10`

```
pip install virtualenv
virtualenv venv
source venv/bin/activate

pip install -r requirements.txt

python -m pytest -m ui --alluredir=./allure-results
```

For local run `.env` file should looks like

```
REMOTE_URL="http://localhost:4444/wd/hub" # if you want to send auto tests to selenium hub, make sure docker-compose running
# REMOTE_URL= # if you want to run auto tests on you machine
BASE_URL="https://www.w3schools.com"
SCREENSHOTS_ON=true
```

**Running in docker**

Assume you have `docker`, `docker-compose` installed

```
docker-compose up
```

As artifact of the auto tests running in the docker container
you will get `allure-results` folder

**Create report**

Run report server locally

```
allure serve
```

Or generate report

```
allure generate
```

This command will create folder `allure-report`. Open `allure-report` folder and open `index.html` file
