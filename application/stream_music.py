import requests
from flask import  Blueprint, jsonify, make_response

music_stream = Blueprint('music_stream', __name__, template_folder='templates')

url = "https://deezerdevs-deezer.p.rapidapi.com/search"

querystring = {"q":"eminem"}

headers = {
    'x-rapidapi-key': "d765230cffmshfbcb0be68220569p1887a6jsn21942133f34b",
    'x-rapidapi-host': "deezerdevs-deezer.p.rapidapi.com"
}



@music_stream.route('/streammusic')
def streammusic():
    response = requests.request("GET", url, headers=headers, params=querystring)
    to_str = response

    return to_str