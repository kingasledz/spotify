from bs4 import BeautifulSoup
import requests
import spotipy




def create_playlist(date,auth_manager):
    url = f"https://www.billboard.com/charts/hot-100/{date}/"
    response = requests.get(url)
    url_text = response.text

    soup = BeautifulSoup(url_text, "html.parser")
    song_names = soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")

    artists = soup.select(selector="div li.lrv-u-width-100p span")
    artist_list = [artist.getText().strip() for artist in artists if not artist.getText().strip().isdigit() if "-" not in artist.getText().strip()] 

    

    song_list = []
    for song in song_names:
        stripped = song.getText().strip()
        song_list.append(stripped)


    sp = spotipy.Spotify(auth_manager=auth_manager)

    user = sp.current_user()["id"]



    song_uris = []
    for i in range(40):
        try:
            track = song_list[i]
            artist = artist_list[i]
            searchQuery = track + " " + artist
            searchResults = sp.search(q=searchQuery,market="US",limit=1)
            final_url = searchResults["tracks"]["items"][0]["uri"]
            song_uris.append(final_url)
        except:
            pass
    



    playlist = sp.user_playlist_create(user=user, name=f"{date} Billboard 40", public=False)
    playlist_id_num = playlist["id"]

    link = playlist["external_urls"]["spotify"]


    sp.playlist_add_items(playlist_id=playlist_id_num, items=song_uris)

    return link
