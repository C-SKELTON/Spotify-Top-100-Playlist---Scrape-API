import pprint
import spotipy
from bs4 import BeautifulSoup
import requests
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv("C:/Users/conno/PycharmProjects/.env.txt")

id = os.getenv("client_id")
password = os.getenv("client_secret")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id = id,
        client_secret = password,
        show_dialog=True,
        cache_path="mytoken.txt"
    )
)
user_id = sp.current_user()["id"]

chosen_date = input("What year do you want to travel to? Type the date in this format YYYY-MM-DD ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{chosen_date}/")

top100_website = response.text
soup = BeautifulSoup(top100_website, "html.parser")
soup.prettify()

year = chosen_date.split("-")[0]
# print(year)
x = [item.getText().strip() for item in soup.select("li ul li h3")]

song_list = []

for y in range(len(x)):
    result = sp.search(q=f"track: {x[y]} year: {year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_list.append(uri)
        #print(y)
        # print(uri)
        # print(song_list)

    except IndexError:
        print(f"{y} doesn't exist in Spotify. Skipped.")



# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(result)
# print(result)

# print(uri)

my_playlist = sp.user_playlist_create(user_id,f"{chosen_date} Billboard Top 100", public=False, collaborative=False)
my_playlist_id = my_playlist["id"]
sp.playlist_add_items(my_playlist_id, song_list)
