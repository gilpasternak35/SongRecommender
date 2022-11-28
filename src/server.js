class Server {

    static URL = "https://acohenar.pythonanywhere.com"

    static async getUserPlaylists(username) {
        return await $.ajax({
            url: Server.URL + "/getplaylists",
            type:"GET",
            dataType: 'json',
            data: {"username": username},
            headers: {'Access-Control-Allow-Origin': '*'},

            success: function(response){
                return response;
            },
            error: function(e){
                return {error: e}
            }
        });
    }

    static async getSongsFromPlaylist(username, playlist) {
        return await $.ajax({
            url: Server.URL + "/getsongs",
            type:"GET",
            dataType: 'json',
            data: {"username": username, "playlist": playlist},
            headers: {'Access-Control-Allow-Origin': '*'},

            success: function(response){
                return response;
            },
            error: function(e){
                return {error: e}
            }
        });
    }
}