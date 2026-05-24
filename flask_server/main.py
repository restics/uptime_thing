from flask import Flask, request
from flask_cors import CORS

from db import CardRepository
from service import CardService
from logger import logger

app = Flask(__name__)
CORS(app)
card_service = CardService(delay=20)
card_repo = card_service.repository # bad rpactice but im lazy rn

@app.route("/card/<id>", methods=['GET', 'DELETE', 'PUT'])
def search(id):
    if request.method == 'GET':
        res = card_repo.get_card_by_id(id)
        return res if res else {}
    if request.method == 'DELETE':
        return card_repo.del_card_by_id(id)
    elif request.method == 'PUT':
        return card_repo.update_card(**request.get_json())
    
@app.route("/cards",  methods=['GET'])
def list_cards():
    res = card_repo.get_all_cards()
    return [card.to_json() for card in res] if res else []
@app.route("/cards/create", methods=['POST'])
def create_card():
    return card_repo.add_card(**request.get_json())

if __name__ == "__main__":

    app.run(debug=True)
    