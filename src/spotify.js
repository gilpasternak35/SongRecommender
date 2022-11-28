class Spotify {
    static async getPlaylistsByUser(user, authToken) {

        return await $.ajax({
            url: `https://api.spotify.com/v1/users/${user}/playlists?limit=40`,
            headers: {
                Authorization: "Bearer " + authToken
            },
            accepts: "application/json",
            type: "GET",
            success: function (data) {
                return data;
            },
            error: function (data) {
                return {error: data};
            }
        });
    }

    static async getTracksInPlaylist(playlist, authToken) {
        return await $.ajax({
            url: `https://api.spotify.com/v1/playlists/${playlist}/tracks`,
            headers: {
                Authorization: "Bearer " + authToken
            },
            accepts: "application/json",
            type: "GET",
            success: function (data) {
                return data;
            },
            error: function (data) {
                return {error: data};
            }
        });
    }
}
