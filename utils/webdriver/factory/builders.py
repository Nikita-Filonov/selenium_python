from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from seleniumwire import webdriver as wire_driver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.webdriver.factory.browser import Browser
from utils.webdriver.factory.capabilities import build_capabilities
from utils.webdriver.factory.options import build_options


def build_chrome(
    version: str | None,
    options: list[str] | None,
    capabilities: dict | None,
    experimental_options: list[dict],
    seleniumwire_options: dict | None,
    extension_paths: list[str] | None,
    local_path: str | None,
    webdriver_kwargs: dict | None,
):
    """Build a Chrome WebDriver.

    Args:
        version: The desired version of Chrome.
        options: The list of options/arguments to include.
        capabilities: The dict of capabilities to include.
        experimental_options: The list of experimental options to include.
        seleniumwire_options: The dict of seleniumwire options to include.
        extension_paths: The list of extension filepaths to add to the browser.
        local_path: The path to the driver binary (only to bypass WebDriverManager)
        webdriver_kwargs: additional keyword arguments to pass.

    Usage:
        driver = webdriver_factory.build_chrome("latest", ["headless", "incognito"])
    """
    wire_options = seleniumwire_options or {}
    browser_options = build_options(
        Browser.CHROME, options, experimental_options, extension_paths
    )
    capabilities = build_capabilities(Browser.CHROME, capabilities)

    for capability in capabilities:
        browser_options.set_capability(capability, capabilities[capability])

    service = ChromeService(
        local_path or ChromeDriverManager(version=version).install()
    )
    driver = wire_driver.Chrome(
        service=service,
        options=browser_options,
        seleniumwire_options=wire_options,
        **(webdriver_kwargs or {}),
    )

    # enable Performance Metrics from Chrome Dev Tools
    driver.execute_cdp_cmd("Performance.enable", {})
    return driver


def build_firefox(
    version: str | None,
    options: list[str] | None,
    capabilities: dict | None,
    experimental_options: list[dict] | None,
    seleniumwire_options: dict | None,
    extension_paths: list[str] | None,
    local_path: str | None,
    webdriver_kwargs: dict | None,
):
    """Build a Firefox WebDriver.

    Args:
        version: The desired version of Firefox.
        options: The list of options/arguments to include.
        capabilities: The dict of capabilities to include.
        experimental_options: The list of experimental options to include.
        seleniumwire_options: The dict of seleniumwire options to include.
        extension_paths: The list of extensions to add to the browser.
        local_path: The path to the driver binary.
        webdriver_kwargs: additional keyword arguments to pass.

    Usage:
        driver = webdriver_factory.build_firefox("latest", ["headless", "incognito"])
    """
    wire_options = seleniumwire_options or {}
    capabilities = build_capabilities(Browser.FIREFOX, capabilities)
    browser_options = build_options(
        Browser.FIREFOX, options, experimental_options, extension_paths
    )

    service = FirefoxService(
        local_path or GeckoDriverManager(version=version).install()
    )
    return wire_driver.Firefox(
        service=service,
        capabilities=capabilities,
        options=browser_options,
        seleniumwire_options=wire_options,
        **(webdriver_kwargs or {}),
    )


def build_remote(
    browser: Browser,
    remote_url: str,
    options: list[str] | None,
    capabilities: dict | None,
    experimental_options: list[dict] | None,
    extension_paths: list[str] | None,
    webdriver_kwargs: dict | None,
):
    """Build a RemoteDriver connected to a Grid.

    Args:
        browser: Name of the browser to connect to.
        remote_url: The URL to connect to the Grid.
        options: The list of options/arguments to include.
        capabilities: The dict of capabilities to include.
        experimental_options: The list of experimental options to include.
        extension_paths: The list of extensions to add to the browser.
        webdriver_kwargs: additional keyword arguments to pass.

    Usage:
        driver = webdriver_factory.build_remote("chrome", "http://localhost:4444/wd/hub", ["headless"])

    Returns:
        The instance of WebDriver once the connection is successful
    """
    capabilities = build_capabilities(browser, capabilities)
    browser_options = build_options(
        browser, options, experimental_options, extension_paths
    )

    for capability in capabilities:
        browser_options.set_capability(capability, capabilities[capability])

    return webdriver.Remote(
        command_executor=remote_url,
        options=browser_options,
        **(webdriver_kwargs or {}),
    )
