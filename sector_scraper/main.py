from playwright.sync_api import Playwright, sync_playwright, expect
#from .parse import get_data
from dotenv import load_dotenv 
import os

load_dotenv()

url = os.getenv("SECTOR-URL")
user = os.getenv("SECTOR-MAIL")
passwd = os.getenv("SECTOR-PASSWORD")


def write_to_file(filename: str, page_content):
    with open(f"output/{filename}", "w") as f:
        f.write(page_content)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False) # make this optional
    context = browser.new_context()
    try:
        page = context.new_page()
        page.goto(f"https://{url}")
        page.get_by_label("E-mail*").click()
        page.get_by_label("E-mail*").fill(f"{user}")
        page.get_by_label("E-mail*").press("Tab")
        page.get_by_label("Password*").click()
        page.get_by_label("Password*").fill(f"{passwd}")
        page.get_by_role("button", name="Log in").click()
        page.get_by_role("link", name="Temperatur").click()
        expect(page.get_by_text("TillbakaTemperaturHär är alla")).to_be_visible()
        page_content = page.content()

        write_to_file("output.html", page_content)

    except Exception as e:
        print(f"Error here: {e}")
    
    finally:
        context.close()
        browser.close()

def main():
    fetch_latest = True
    if fetch_latest:
        with sync_playwright() as playwright:
            run(playwright)
    
    #get_data()


if __name__ == "__main__":
    main()
