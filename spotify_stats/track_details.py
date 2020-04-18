import json

class TrackDetails(object):
    def serialize(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.serialize()

    def __init__(self):
        self.title = None
        self.artist = None
        self.duration = None
        self.danceability = None
        self.energy = None
        self.loudness = None
        self.speechiness = None
        self.instrumentalness = None
        self.valence = None
        self.tempo = None
        self.time_signature = None
        self.key = None
