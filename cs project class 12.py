import random
import pylast
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import time
import csv
import mysql.connector

user_id=int(input("enter user id"))

connection = mysql.connector.connect(host="localhost", user="root", passwd="08L6lx9Wn$%!")
if connection.is_connected():
    print("successful")
cursor = connection.cursor()

# Function to insert user interaction into the MySQL database
def log_user_interaction(user_id, action_type, action_details):
    connection = mysql.connector.connect(host="localhost", user="root", passwd="08L6lx9Wn$%!")

    cursor = connection.cursor()

    # Create the 'music_bot_db' database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS music_bot_db")

    # Switch to the 'music_bot_db' database
    cursor.execute("USE music_bot_db")

    # Create the 'user_history' table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            action_type VARCHAR(255),
            action_details TEXT
        )
    """)

    # Now insert the user interaction into the table
    query = "INSERT INTO user_history (user_id, action_type, action_details) VALUES (%s, %s, %s)"
    values = (user_id, action_type, action_details)
    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()


# API key and secret for Last.fm
API_KEY = 'd36bd24296733f9a0dc2c33a193338c8'
API_SECRET = 'd5fae53eaf13aa62970a0f8934c1d8b4'
lastfm = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

# Spotify API credentials
SCOPE = 'playlist-modify-private'
REDIRECT_URI = 'http://localhost:8000/callback'

sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id='e0b4adca73d547f28ed445cd46b0048c', client_secret='b823ecf3e2074cf0946fd9fd8a41c980', redirect_uri=REDIRECT_URI, scope=SCOPE)
# Get the authorization URL
auth_url = sp_oauth.get_authorize_url()
webbrowser.open(auth_url, new=2)
auth_code = input("Enter the authorization code from the redirect URI: ")
# Obtain the access token
token_info = sp_oauth.get_cached_token()

if token_info is None or sp_oauth.is_token_expired(token_info):
    # Token is expired or not available, perform the authorization process
    auth_url = sp_oauth.get_authorize_url()
    webbrowser.open(auth_url, new=2)
    auth_code = input("Enter the authorization code from the redirect URI: ")

    # Obtain the access token using the authorization code
    token_info = sp_oauth.get_access_token(auth_code)

# Rest of your code using the access token
access_token = token_info['access_token']
sp = spotipy.Spotify(auth=access_token)

playlist = {}

# List with all sad quotes
quotes_sad = [
    "Tears are words the heart can't express.",
    "The world is full of songs. The air is living with its music.",
    "Sometimes the songs that we hear are just song of our own.",
    "The sound of music has a powerful way of evoking memories and feelings.",
    "A song can lift your spirit, warm the heart and soothe the soul.",
    "Listening to music is like taking a journey into someone else's soul.",
    "Music is the silence between the notes.",
    "Music is the art which is most nigh to tears and memories.",
    "Music has a way of speaking what cannot be expressed.",
    "Music has the power to heal the soul."
]

# List with all happy quotes
quotes_positive = [
    "Life is one grand, sweet song, so start the music.",
    "Let your heart dance to the beat of your dreams.",
    "The rhythm of life is a beautiful song, don't miss a beat.",
    "Happiness is having a large, loving, caring, close-knit family in another city.",
    "A smile is a curve that sets everything straight.",
    "Happiness is a warm puppy.",
    "The greatest happiness you can have is knowing that you do not necessarily require happiness.",
    "Laughter is the sun that drives winter from the human face.",
    "Happiness is not something you postpone for the future; it is something you design for the present.",
    "Joy is not in things; it is in us."
]

# Function to get a random quote
def get_random_quote(mood):
    if mood == "happy":
        return random.choice(quotes_positive)
    elif mood == "sad":
        return random.choice(quotes_sad)
    else:
        return None

# Printing the starting line
print("Welcome to a simple music chat bot")

# Starting the menu-driven program
ask = "yes"
# Inside the main loop
while ask == "yes":
    print("1. Recommend songs according to your mood")
    print("2. Create a playlist")
    print("3. Add songs to the above playlist")
    print("4. Top Tracks of the Month")
    print("5. User History")

    n = int(input("Enter your choice: "))

    if n == 1:
        print("\nHello User!\nHow are you feeling today?")
        user_input = input("")

        if user_input.lower() in ["ecstatic", "good", "elated", "joyful", "cheerful", "thrilled", "blissful", "pleased",
                          "radiant", "overjoyed", "grinning", "beaming", "exuberant", "dancing", "smiling",
                          "jolly", "grateful", "amazing", "excited", "content", "upbeat", "happy",
                          "jubilant", "vibrant", "merry", "delighted", "radiant", "optimistic", "ecstatic",
                          "euphoric", "exhilarated", "content", "sunny", "buoyant", "joyous", "elated",
                          "overjoyed"]:
            print("That's amazing!\n")
            mood = "happy"
        elif user_input.lower() in ["depressed", "disheartened", "downcast", "forlorn", "gloomy", "melancholic",
                        "miserable", "pessimistic", "sorrowful", "suicidal", "weepy", "blue", "despondent",
                        "heartbroken", "lonely", "nostalgic", "regretful", "wistful", "desolate",
                        "devastated", "sad", "bad", "angry", "somber", "dismal", "lamenting", "downhearted",
                        "woeful", "heartrending", "disconsolate", "desolate", "crestfallen", "mournful",
                        "melancholy", "forlorn", "pensive", "tragic", "teary-eyed", "heavyhearted",
                        "grief-stricken", "defeated", "dejected", "despondent"]:
            mood = "sad"
        else:
            mood = None

        if mood is not None:
            print(get_random_quote(mood))
            print("Hope you can improve your day with some music")
            print("Here's some music you may like:\n")

            # Search for playlists based on a keyword related to the mood
            results = sp.search(q=mood, type='playlist', limit=10)

            # Iterate over the playlist items
            for i, playlist in enumerate(results['playlists']['items']):
                playlist_name = playlist['name']
                playlist_url = playlist['external_urls']['spotify']
                print(str(i + 1) + ". " + playlist_name + " - " + playlist_url)
                time.sleep(0.3)

            # Ask the user to select a playlist
            print("\n")
            selected_playlist_number = input("Select a playlist by its number: ")

            # Retrieve the selected playlist and its tracks
            selected_playlist_index = int(selected_playlist_number) - 1
            selected_playlist = results['playlists']['items'][selected_playlist_index]
            selected_playlist_id = selected_playlist['id']
            selected_playlist_tracks = sp.playlist_tracks(playlist_id=selected_playlist_id, limit=10)

            # Display the list of tracks to the user
            for i, track in enumerate(selected_playlist_tracks['items']):
                track_name = track['track']['name']
                track_artist = track['track']['artists'][0]['name']
                print(str(i + 1) + ". " + track_name + " by " + track_artist)
                time.sleep(0.3)

            # Ask the user to select a song
            print("\n")
            selected_song_number = input("Select a song by its number: ")

            # Play the selected song or redirect the user to its page on Spotify
            selected_song_index = int(selected_song_number) - 1
            selected_song = selected_playlist_tracks['items'][selected_song_index]['track']
            selected_song_name = selected_song['name']
            selected_song_artist = selected_song['artists'][0]['name']
            selected_song_url = selected_song['external_urls']['spotify']
            print("Your selected song is '" + selected_song_name + "' by '" + selected_song_artist + "'")

            webbrowser.open(selected_song_url, new=2)

        else:
            print("Sorry, I couldn't recognize your mood. Here are some random songs:")
            results = sp.search(q="hindi and english", type='playlist', limit=10)

            # Iterate over the playlist items
            for i, playlist in enumerate(results['playlists']['items']):
                playlist_name = playlist['name']
                playlist_url = playlist['external_urls']['spotify']
                print(str(i + 1) + ". " + playlist_name + " - " + playlist_url)
                time.sleep(0.3)

            # Ask the user to select a playlist
            print("\n")
            selected_playlist_number = input("Select a playlist by its number: ")

            # Retrieve the selected playlist and its tracks
            selected_playlist_index = int(selected_playlist_number) - 1
            selected_playlist = results['playlists']['items'][selected_playlist_index]
            selected_playlist_id = selected_playlist['id']
            selected_playlist_tracks = sp.playlist_tracks(playlist_id=selected_playlist_id, limit=10)

            # Display the list of tracks to the user
            for i, track in enumerate(selected_playlist_tracks['items']):
                track_name = track['track']['name']
                track_artist = track['track']['artists'][0]['name']
                print(str(i + 1) + ". " + track_name + " by " + track_artist)
                time.sleep(0.3)

            # Ask the user to select a song
            print("\n")
            selected_song_number = input("Select a song by its number: ")

            # Play the selected song or redirect the user to its page on Spotify
            selected_song_index = int(selected_song_number) - 1
            selected_song = selected_playlist_tracks['items'][selected_song_index]['track']
            selected_song_name = selected_song['name']
            selected_song_artist = selected_song['artists'][0]['name']
            selected_song_url = selected_song['external_urls']['spotify']
            print("Your selected song is '" + selected_song_name + "' by '" + selected_song_artist + "'")


            webbrowser.open(selected_song_url, new=2)

    elif n == 2:
        print("\nCreating a new playlist...\n")

        # Authenticating the user
        playlist_name = input("Enter the playlist name: ")
        playlist_description = input("Enter the playlist description: ")
        playlist_public = input("Should the playlist be public? (yes/no): ")

        # Create the playlist
        playlist = sp.user_playlist_create(sp.me()["id"], name=playlist_name, public=(playlist_public.lower() == "yes"),
                                           description=playlist_description)

        print("Playlist created successfully!")
        print("Playlist ID:", playlist["id"])
        print("Playlist URL:", playlist["external_urls"]["spotify"])

        log_user_interaction(user_id, 'Playlist Creation', f'Created playlist: {playlist_name}')

        # Open the playlist URL in a web browser
        webbrowser.open(playlist["external_urls"]["spotify"])

    elif n == 3:
        genre = input("Enter the genre of songs you'd like to select: ")
        track_results = sp.search(q='genre:"' + genre + '"', type='track', limit=10)

        print("Here are some tracks in the", genre, "genre:")
        for i, track in enumerate(track_results['tracks']['items']):
            print(i + 1, "-", track['name'], "by", track['artists'][0]['name'])

        track_numbers = input("Enter the track numbers (separated by commas) that you'd like to add to the playlist: ")
        track_numbers = [int(num.strip()) for num in track_numbers.split(',')]

        tracks_to_add = [track_results['tracks']['items'][num - 1] for num in track_numbers]
        track_uris = [track['uri'] for track in tracks_to_add]

        # Add the selected tracks to the playlist
        sp.playlist_add_items(playlist["id"], track_uris)

        # Save the track details to a CSV file
        filename = playlist_name + "_tracks.csv"
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Track Name", "Artist", "Album"])
            for track in tracks_to_add:
                writer.writerow([track['name'], track['artists'][0]['name'], track['album']['name']])

        print("Selected tracks have been added to the playlist.")
        print("Track details have been saved to", filename)

        # Open the playlist URL in a web browser
        webbrowser.open(playlist["external_urls"]["spotify"])

        # Display the playlist from the CSV file
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            print("\nPlaylist from CSV:")
            for row in reader:
                print("Track Name:", row[0])
                print("Artist:", row[1])
                print("Album:", row[2])
                print()

    elif n == 4:
        # Get list of top tracks of the month
        print("\nTOP TRACKS OF THE MONTH\n")
        top_tracks = lastfm.get_top_tracks()

        # Display the list of songs to the user
        for i, top_item in enumerate(top_tracks[:10]):
            track = top_item.item
            print(i + 1, "-", track.get_name(), "by", track.get_artist().get_name())

        # Log the user interaction for menu choices
        log_user_interaction(user_id, 'Menu Choice', 'User checked Top Tracks of the Month')

    elif n == 5:
        # Display user history
        print("\nUSER HISTORY\n")
        # Fetch and display user history from the database
        connection = mysql.connector.connect(host="localhost",user="root",passwd="08L6lx9Wn$%!",db="music_bot_db" )
        cursor = connection.cursor()
        # Fetch user history for the current user
        cursor.execute("SELECT action_type, action_details FROM user_history WHERE user_id = %s", (user_id,))
        user_history = cursor.fetchall()
        if user_history:
            print("User History:")
            for i, (action_type, action_details) in enumerate(user_history):
                print(f"{i + 1}. {action_type} - {action_details}")
        else:
            print("No user history available.")
        cursor.close()
        connection.close()
        # Log the user interaction for menu choice 5
        log_user_interaction(user_id, 'Menu Choice', 'User checked User History')

    ask = input("\nWould you like to continue? (Yes/No):")
