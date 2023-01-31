def main():
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    import spotipy.util as util
    import os

    def execute(choice):
        os.environ["SPOTIPY_CLIENT_ID"]='SPOTIPY_CLIENT_ID'
        os.environ["SPOTIPY_CLIENT_SECRET"]='SPOTIPY_CLIENT_SECRET'
        os.environ["SPOTIPY_REDIRECT_URI"]='SPOTIPY_REDIRECT_URI'
        
        scope = "user-library-read"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        if choice == 0:
            from datetime import datetime

            results = sp.current_user_saved_tracks()
            curDT = datetime.now()
            date_time = curDT.strftime("%d_%m_%Y_%H_%M_%S")

        if choice == 1:
            import datetime

            results = sp.playlist_tracks("PLAYLIST_SHARE_LINK")
            my_date = datetime.date.today()
            year, week_num, day_of_week = my_date.isocalendar()
            date_time = f"{year}_WEEK_{week_num}"

        songs = results['items']

        while results['next']:
            results = sp.next(results)
            songs.extend(results['items'])

        uris = []
        with open(paths[choice]+date_time+".log","w", encoding="UTF-8") as f:
            for idx, item in enumerate(songs):
                track = item['track']
                f.write(str(idx)+" -> "+track['artists'][0]['name']+ " - "+ track['name']+"\n")
                uris.append(track["uri"])

        with open(paths[choice]+date_time+"_URI.log","w", encoding="UTF-8") as f:
            for uri in uris:
                f.write(str(uri).split(":")[-1]+"\n")
        
    paths = ["Tasks/SpotifyBackup/Output/LIKED/","Tasks/SpotifyBackup/Output/WEEK/"]

    if not os.path.exists("Tasks/SpotifyBackup/Output/"):
        os.mkdir("Tasks/SpotifyBackup/Output/")
        
    if not os.path.exists(paths[0]):
        os.mkdir(paths[0])
    
    if not os.path.exists(paths[1]):
        os.mkdir(paths[1])

    execute(0)
    execute(1)

    return "SpotifyBackup task completed successfully"

def initialize():
    return "SpotifyBackup initialized"

if __name__ == "__main__":
    main()
