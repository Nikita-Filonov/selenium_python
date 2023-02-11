import allure

from utils.webdriver.driver.page import Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def visit(self, url: str) -> Page:
        with allure.step(f'Opening the url "{url}"'):
            return self.page.visit(url)

    def reload(self) -> Page:
        page_url = self.page.url()
        with allure.step(f'Reloading page with url "{page_url}"'):
            return self.page.reload()
