import json

from flask import Flask, request, jsonify, redirect
from spotify_stats import playlist_url_to_id, playlist_id_to_track_list, track_list_to_details

app = Flask(__name__, static_url_path='/')

@app.route('/')
def index():
    return redirect('index.html')

@app.route('/playlist/')
def playlist_data():
    url = request.args.get('url', None)
    if url is None:
        return jsonify({'tracks': []})
    playlist_id = playlist_url_to_id(url)
    track_list = playlist_id_to_track_list(playlist_id)
    details = track_list_to_details(track_list)
    details = [json.loads(str(detail)) for detail in details]
    return jsonify({'tracks': details})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
