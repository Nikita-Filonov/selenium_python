import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webdriver import WebElement
from utils.types.webdriver.driver.waiting import WebElementUntilMethod


class ElementWait:
    def __init__(self, webelement: WebElement, timeout: int, ignored_exceptions: list = None):
        self._webelement = webelement
        self._timeout = 10 if timeout == 0 else timeout

        if ignored_exceptions:
            self._ignored_exceptions = ignored_exceptions
        else:
            self._ignored_exceptions = NoSuchElementException

    def until(self, method: WebElementUntilMethod, message=""):
        screen = None
        stacktrace = None

        end_time = time.time() + self._timeout
        while True:
            try:
                value = method(self._webelement)
                if value:
                    return value
            except self._ignored_exceptions as exc:
                screen = getattr(exc, "screen", None)
                stacktrace = getattr(exc, "stacktrace", None)

            time.sleep(0.5)
            if time.time() > end_time:
                break

        raise TimeoutException(message, screen, stacktrace)
