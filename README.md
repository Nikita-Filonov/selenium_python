# Selenium python

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

**Running in docker**

Assume you have `docker`, `docker-compose` installed

```
docker-compose up
```

**Create report**

```
allure serve

or

allure generate
```
