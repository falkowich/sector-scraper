from bs4 import BeautifulSoup


def parse_temperature(filename: str):
    soup = BeautifulSoup(open(f"output/{filename}", encoding="utf8"), "html.parser")

    heading = soup.find("h1", string="Temperatur")
    if heading is None:
        print("No Temperature heading found")
        return

    parent_div = heading.find_parent("div", class_="pgTwo")
    if parent_div is None:
        print("No parent_div with class pgTwo found")
        return

    area_containers = parent_div.find_all("div", class_="qa-area-container")
    if area_containers is None:
        print("No area_containers found")
        return

    for container in area_containers:
        area_name = container.find("h3", class_="qa-area-name").text
        tiles = container.find_all("div", role="tile")

        for tile in tiles:
            temperature = tile.find("div", class_="qa-place-average-temperature").text
            place_name = tile.find("h3", class_="qa-place-name").text
            print(f"Area: {area_name}, Room: {place_name}, Temperature: {temperature}")
