import allure

from utils.webdriver.client import AppWebDriver


class BasePage:
    def __init__(self, client: AppWebDriver) -> None:
        self.client = client

    def visit(self, url: str) -> AppWebDriver:
        with allure.step(f'Opening the url "{url}"'):
            return self.client.visit(url)

    def reload(self) -> AppWebDriver:
        page_url = self.client.url()
        with allure.step(f'Reloading page with url "{page_url}"'):
            return self.client.reload()
