class Server {

    //static URL = "https://acohenar.pythonanywhere.com"
    static URL = "http://localhost:5000"

    static getAuthToken() {
        if (Server.authToken && new Date().getTime() / 1000 < Server.authExpiry) {
            return Server.authToken;
        }
        var SPOTIPY_CLIENT_ID = "a33300f31485436eb86addeadd1eb614"
        var SPOTIPY_REDIRECT_URI = Server.URL + "/callback"
        var spotifyScope = "playlist-read-private"
        var spotifyAuthEndpoint = "https://accounts.spotify.com/authorize?"+"client_id="+SPOTIPY_CLIENT_ID+"&redirect_uri="+SPOTIPY_REDIRECT_URI+"&scope="+spotifyScope+"&response_type=token&state=123";
        window.open(spotifyAuthEndpoint, 'callBackWindow','height=500,width=400');
        window.addEventListener("message", async function(event){
            if (!event) return;
            Server.authToken = event.data;
            Server.authExpiry = new Date().getTime() / 1000 + 3600

            return await $.ajax({ 
                url: `https://api.spotify.com/v1/me`,
                headers: {
                    'Authorization': "Bearer " + Server.authToken,
                },
                accepts: "application/json",
                type: "GET",
                success: function (data) {
                    Server.currentUserProfile = data;
                    return data;
                },
                error: function (data) {
                    return {error: data};
                }
            });
        });
    }
}