import requests
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass

URL_TO_SCRAPING = "https://mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_courses(blocks: list[Tag]) -> list[Course]:
    courses = []

    for block in blocks:
        paragraphs = block.select("p")
        duration = paragraphs[0].get_text(strip=True)
        short_description = paragraphs[1].get_text(strip=True)
        name = block.select_one("h3").get_text(strip=True)

        courses.append(Course(
            name=name,
            short_description=short_description,
            duration=duration
        ))

    return courses


def get_all_courses() -> list[Course]:
    response = requests.get(URL_TO_SCRAPING)
    soup = BeautifulSoup(response.content, "html.parser")

    blocks = soup.select(".ProfessionCard_content__mPiVi")
    return parse_courses(blocks)


if __name__ == "__main__":
    print(get_all_courses())
