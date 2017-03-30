/**
 * Created by d1md1m on 30.03.17.
 */

function progress(percent, $element) {
  var progressBarWidth = percent * $element.width() / 100;

// $element.find('div').animate({ width: progressBarWidth }, 500).html(percent + "%&nbsp;");

  $element.find('div').animate({ width: progressBarWidth });
}

var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;

function onYouTubeIframeAPIReady() {
    player = new YT.Player('ytplayer', {
      height: '540',
      width: '960',
      videoId: 'UDxzMcCrOyI',
        playerVars: {
        'controls' : 0,
        'modestbranding' : 1,
        'rel' : 0,
        'showinfo' : 0
      },
        events: {
            'onReady': onPlayerReady,
             'onStateChange': onPlayerStateChange
        }
    });
}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
    event.target.playVideo();
}

// 5. The API calls this function when the player's state changes.
//    The function indicates that when playing a video (state=1),
//    the player should play for six seconds and then stop.

function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING) {

      $('#progressBar').show();
      var playerTotalTime = player.getDuration();

      mytimer = setInterval(function() {
        var playerCurrentTime = player.getCurrentTime();

        var playerTimeDifference = (playerCurrentTime / playerTotalTime) * 100;


        progress(playerTimeDifference, $('#progressBar'));
      }, 1000);
    } else {

      clearTimeout(mytimer);
      $('#progressBar').hide();
    }
}



function stopVideo() {
    player.stopVideo();
}