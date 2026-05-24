from db import CardRepository, Card

def test_add_and_get_card():
    # Arrange
    repo = CardRepository()
    
    # Act
    repo.add_card(name="Google", url="https://google.com")
    card = repo.get_card_by_id(1)
    
    # Assert
    assert card.name == "Google"
    assert card.url == "https://google.com"
    assert card.status == "UPDATING"


def test_update_card():
    # Arrange
    repo = CardRepository()
    
    # Act
    repo.add_card(name="Google", url="https://google.com")
    repo.update_card(Card())
    card = repo.get_card_by_id(1)
    
    # Assert
    assert card.name == "Google"
    assert card.url == "https://google.com"
    assert card.status == "UPDATING"