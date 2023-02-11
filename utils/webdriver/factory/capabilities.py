from selenium import webdriver

from utils.webdriver.factory.browser import Browser

Capabilities = dict[str, str]


def build_capabilities(browser: Browser, capabilities: Capabilities | None) -> Capabilities:
    """Build the capabilities dictionary for the given browser.

    Some WebDrivers pass in capabilities directly, but others (ie Chrome) require it be added via the Options object.

    Args:
        browser: The name of the browser.
        capabilities: The dict of capabilities to include. If None, default caps are used.

    Usage:
        caps = build_capabilities("chrome", {"enableVNC": True, "enableVideo": False})
    """
    capabilities: Capabilities = {}

    match browser:
        case Browser.CHROME:
            capabilities.update(webdriver.DesiredCapabilities.CHROME.copy())
        case     Browser.FIREFOX:
            capabilities.update(webdriver.DesiredCapabilities.FIREFOX.copy())
        case _:
            raise ValueError(
                f"{browser} is not supported. Cannot build capabilities."
            )

    if capabilities:
        capabilities.update(capabilities)

    return capabilities
