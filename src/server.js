class Server {
    static async getUserPlaylists(username) {
        return await $.ajax({
            url:"http://127.0.0.1:5000/getplaylists",
            type:"GET",
            dataType: 'json',
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
            url:"http://127.0.0.1:5000/getsongs",
            type:"GET",
            dataType: 'json',
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