import json

with open('./assets/chunithm/data/music-ex.json', 'r', encoding='utf-8') as f:
    music_data = json.load(f)

async def get_song_by_id(song_id: str):
    for song in music_data:
        if song['id'] == song_id:
            return song
    return None

