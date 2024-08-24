# Music Recommender

## Project Overview
This repository contains the code and resources for our Class 12 Computer Science project, "Music Recommender." This project was developed collaboratively by our team using Scratch and various advanced technologies to create an intelligent system that provides personalized song recommendations based on the user's mood.

## Project Description
In the realm of personalized music discovery, the integration of advanced technologies has led to the creation of innovative tools for curating and recommending songs tailored to individual preferences. This project embarks on the journey of developing a music recommender, an intelligent system that harnesses the power of natural language processing and music analysis.

By leveraging Python, the Spotify API, the LastFM API, and integrating MySQL, the project aims to provide users with a seamless and engaging music recommendation experience. Unlike traditional methods that rely solely on user history or genre preferences, our approach uses the tone and mood of the user's conversation to guide song recommendations.

## Features
- **Mood Recognition:** Analyzes the user's conversation to identify their emotional state using natural language processing techniques.
- **Spotify Integration:** Connects to the Spotify database using the Spotipy library, providing access to a vast collection of songs and playlists.
- **Mood-Based Playlists:** Recommends playlists that align with the user's emotional context.
- **Song Selection:** Allows users to dive deeper into music that resonates with their mood.
- **Custom Playlist Creation:** Facilitates the creation of personalized playlists based on user preferences.
- **Top Tracks of the Month:** Displays trending music using data from the LastFM API.

## Technologies Used
- **Python**: The primary programming language used for the project.
- **Spotipy**: A Python library for integrating with the Spotify Web API.
- **Pylast**: A Python interface to Last.fm's API.
- **MySQL**: Used for storing user interactions and recommended song details.
- **CSV**: For saving and retrieving track details during playlist creation.

## How to Run the Project
1. Clone this repository to your local machine.
2. Install the required Python libraries:
   pip install spotipy pylast mysql-connector-python
3. Set up API keys for Spotify and LastFM.
4. Configure MySOL for user data storage.
5. Run the Python script to start the Music Recommender.

## Team Members
**-Nandhagopan Babu:** API Setup and User Interaction
**-Rishi Raj:** Playlist Creation, Song Addition, and MySQL Connectivity
**-Pranav Vinod:** Music Recommendations and Top Tracks

## Acknowledgements
We would like to thank our Computer Science teacher for guiding us throughout the project and providing valuable feedback. Special thanks to our classmates and friends for their support.
