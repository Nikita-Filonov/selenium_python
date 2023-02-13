import allure

from components.cookies_modal import CookiesModal
from utils.webdriver.driver.page import Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.cookies_modal = CookiesModal(page)

    def visit(self, url: str) -> None:
        with allure.step(f'Opening the url "{url}"'):
            self.page.visit(url)
            self.cookies_modal.accept_cookies()

    def reload(self) -> Page:
        page_url = self.page.url()
        with allure.step(f'Reloading page with url "{page_url}"'):
            return self.page.reload()
