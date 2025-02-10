from spotify_integration import get_spotify_client

def delete_mood_playlists():
    """Delete all playlists with 'mood' in the title"""
    # Get Spotify client
    sp = get_spotify_client()
    if not sp:
        print("Failed to connect to Spotify")
        return

    try:
        # Get current user's playlists
        results = sp.current_user_playlists()
        playlists = results['items']
        
        # Keep track of deleted playlists
        deleted_count = 0

        # Iterate through playlists and delete those with 'mood' in the name
        for playlist in playlists:
            if 'Mood' in playlist['name']:
                print(f"Deleting playlist: {playlist['name']}")
                sp.current_user_unfollow_playlist(playlist['id'])
                deleted_count += 1

        print(f"\nDeleted {deleted_count} mood playlists")

    except Exception as e:
        print(f"Error deleting playlists: {str(e)}")

if __name__ == "__main__":
    delete_mood_playlists() 