class Spotify {
    static async getPlaylistsByUser(user) {
        return await $.ajax({ 
            url: `https://api.spotify.com/v1/me/playlists`,
            headers: {
                'Authorization': "Bearer " + Server.authToken,
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

    static async getTracksInPlaylist(playlist) {
        return await $.ajax({
            url: `https://api.spotify.com/v1/playlists/${playlist}/tracks`,
            headers: {
                Authorization: "Bearer " + Server.authToken
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

    static async getTrack(trackID) {
        return await $.ajax({
            url: `https://api.spotify.com/v1/tracks/${trackID}`,
            headers: {
                Authorization: "Bearer " + Server.authToken
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

    static async getRecommendations(songs) {
        return await $.ajax({
            url: Server.URL + "/getrecommendations",
            type: "GET",
            dataType: 'json',
            data: {"songs": JSON.stringify(songs)},
            headers: {'Access-Control-Allow-Origin': '*'},

            success: function(response){
                return response;
            },
            error: function(e){
                return {error: e}
            }
        });
    }

    static async sendToSpotify(song, artist) {
        let links = await $.ajax({
            url: `https://api.spotify.com/v1/search?q=track:"${song}"%20artist:"${artist}"&type=track`,
            headers: {
                Authorization: "Bearer " + Server.authToken
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
        let link = links["tracks"]["items"][0]["preview_url"];
        window.open(link);
    }
}
