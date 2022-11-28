// Max px of curve: 224, min: 118px

$ = $ || {} // Void jQuery warnings

class UI {

    static centerSize = 20;
    static currentSize = 20;
    static mouseSpeed = 0;
    static distanceFromCenter = 0;

    /**
     * Updates the wave size
     * @param size radius of the wave
     */
    static updateWave(size) {
        let box = $(".box");
        let wave = box.get(0);
        wave.style.setProperty("--size", size + "px");
        wave.style.setProperty("--p", (size / 2) + "px");
        wave.style.setProperty("--R", Math.sqrt(Math.pow(size, 2) + Math.pow(size / 2, 2)) + "px");
        let height = 11 + size / 4;
        box.css("height", height + "vh");
        box.css("top", 50 - height / 2 + "vh");
    }

    /**
     * Fluctuates the wave at a current time based on a sin function
     */
    static fluctuateWave() {
        let x = Date.now() / 200;
        UI.currentSize = (UI.currentSize / 20) * Math.sin(x) + UI.centerSize;
        UI.updateWave(UI.currentSize);
    }

    /**
     * Begins mouse tracking and stores as class variables
     */
    static trackMouse() {
        UI.speeds = [];
        for (let i = 0; i < 25; i++) {
            UI.speeds.push(0);
        }

        document.addEventListener("mousemove", function(ev){
            UI.mouseSpeed = Math.sqrt(Math.pow(ev.movementX, 2) + Math.pow(ev.movementY, 2));
            UI.distanceFromCenter = Math.sqrt(Math.pow(window.innerWidth/2 - ev.pageX, 2) + Math.pow(window.innerHeight/2 - ev.pageY, 2));
        }, false);
    }

    /**
     * Gets current mouse speed, updates the average speed of the mouse
     */
    static updateSpeed() {
        UI.speeds.pop();
        UI.speeds.unshift(UI.mouseSpeed);
        let total = 0;
        for (let i in UI.speeds) {
            total += UI.speeds[i];
        }
        UI.averageSpeed = total / UI.speeds.length;

        UI.centerSize = 20 + Math.sqrt(UI.averageSpeed) * 4;
    }

    /**
     * Updates the center spotify logo size
     */
    static updateLogo() {
        let c = `calc(15vw + ${Math.max(50 - Math.pow(UI.distanceFromCenter / 30, 2), 0)}px)`;
        let logo = $("#spotify-logo");
        logo.css("width", c);
        logo.css("height", c);
    }

    static bindButtons() {
        $("#spotify-logo").on("click", function() {
            UI.onLogoPress();
        });
    }

    /**
     * Starts all the wave interaction intervals
     */
    static startWaveIntervals() {
        UI.trackMouse();
        UI.inter = setInterval(function() {
            UI.fluctuateWave();
            UI.updateSpeed();
            UI.updateLogo();
        }, 10)
    }

    static onLogoPress() {
        Swal.fire({
            title: 'Enter your Spotify Username',
            input: 'text',
            inputAttributes: {
                autocapitalize: 'off'
            },
            confirmButtonText: 'Next',
            confirmButtonColor: "#13ab4c",
            footer: `<a href="#" onclick="UI.whatsMyUsername()">What's my Spotify Username?</a>`,
            preConfirm: async (username) => {
                if (!username) return {error: "NO USERNAME"};
                UI.currentUsername = username;
                return await Server.getUserPlaylists(username);
            },
        }).then((result) => {
            if (result.isConfirmed && !result.value.error) {
                return UI.chooseTrackDialog(result.value.data);
            }
        });
    }

    static whatsMyUsername() {
        window.open("https://www.spotify.com/us/account/overview/?utm_source=spotify&utm_medium=menu&utm_campaign=your_account", '_blank');
    }

    static chooseTrackDialog(playlists) {
        if (!playlists || playlists.length <= 0) {
            Swal.fire({
                icon: 'error',
                title: 'Username Error',
                text: 'That Spotify user has no playlists or does not exist.',
                footer: '<a href="#" onclick="UI.onLogoPress()">Try again</a>'
            });
            return;
        }
        Swal.fire({
            title: 'Choose your playlist',
            input: 'select',
            inputOptions: playlists,
            inputPlaceholder: 'Select a playlist',
            confirmButtonText: 'Find Songs',
            confirmButtonColor: "#13ab4c",
            preConfirm: async (index) => {
                if (!index) return {error: "NO PLAYLIST"};
                return await Server.getSongsFromPlaylist(UI.currentUsername, playlists[index]);
            },
        }).then((result) => {
            if (result.isConfirmed && !result.value.error) {
                UI.showResultingSongs(result.value.data);
            }
        });
    }

    static showResultingSongs(songs) {
        let modalHtml = ""
        console.log(songs)
        for (let i in songs) {
            modalHtml += `<b>${songs[i]["name"]}</b> by ${songs[i]["artist"]}<a href="https://www.youtube.com/results?search_query=${songs[i]["name"]}+by+${songs[i]["artist"]}"><div class="yt-icon"></div></a><br/>`
        }
        Swal.fire({
            title: 'Recommended Songs',
            html: modalHtml,
            showConfirmButton: false,
            width: "50%",
            footer: '<a href="#" onclick="UI.onLogoPress()">Get More Songs</a>'
        });
    }

    static prepLandingPage() {
        setTimeout(UI.bindButtons, 100);
        UI.startWaveIntervals();
    }
}

UI.prepLandingPage();