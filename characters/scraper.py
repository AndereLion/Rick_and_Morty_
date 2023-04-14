import requests
from django.conf import settings

from characters.models import Character


def scrape_characters() -> list[Character]:
    characters = []
    url_to_scrape = settings.RICK_AND_MORTY_API_CHARACTERS_URL
    characters_response = requests.get(url_to_scrape).json()

    while characters_response:
        characters += [
            Character(
                api_id=character.get("id"),
                name=character.get("name"),
                status=character.get("status"),
                species=character.get("species"),
                gender=character.get("gender"),
                image=character.get("image"),
            )
            for character in characters_response.get("results")
        ]
        if characters_response.get("info").get("next"):
            characters_response = requests.get(
                characters_response.get("info").get("next")
            ).json()
        else:
            characters_response = None
    return characters


def save_characters(characters: list[Character]) -> None:
    Character.objects.bulk_create(characters)


def sync_characters_with_api() -> None:
    characters = scrape_characters()
    save_characters(characters)
