import os

from dotenv import load_dotenv
from sector_scraper.parser import parse_temperature
from sector_scraper.sender import update_sensors
from playwright.sync_api import Playwright, expect, sync_playwright

load_dotenv()

url = os.getenv("SECTOR-URL")
user = str(os.getenv("SECTOR-MAIL"))
passwd = str(os.getenv("SECTOR-PASSWORD"))
env = os.getenv("ENV")
filename = str(os.getenv("FILENAME"))
hoas_url = str(os.getenv("HOMEASSISTANT_URL"))
hoas_token = str(os.getenv("HOMEASSISTANT_TOKEN"))


def write_to_file(filename: str, page_content: str):
    with open(f"output/{filename}", "w") as f:
        f.write(page_content)


def run(playwright: Playwright, filename: str) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    try:
        page = context.new_page()
        page.goto(f"https://{url}")
        page.get_by_label("E-mail*").click()
        page.get_by_label("E-mail*").fill(user)
        page.get_by_label("E-mail*").press("Tab")
        page.get_by_label("Password*").click()
        page.get_by_label("Password*").fill(passwd)
        page.get_by_role("button", name="Log in").click()
        page.get_by_role("link", name="Temperatur").click()
        expect(page.get_by_text("TillbakaTemperaturHär är alla")).to_be_visible()
        page_content = page.content()

        write_to_file(filename, page_content)

    except Exception as e:
        print(f"Error here: {e}")

    finally:
        context.close()
        browser.close()


def main():
    fetch_latest = True
    if fetch_latest:
        with sync_playwright() as playwright:
            run(playwright, filename)

    temperature_lst = parse_temperature(filename)

    update_sensors(temperature_lst, hoas_url, hoas_token)




if __name__ == "__main__":
    main()
