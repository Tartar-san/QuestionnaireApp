/**
 * Created by D1mD1m on 2/8/2017.
 */




function setCookiesLikeTrue() {
    document.cookie = "Like=true";
    console.log("Like=true")
}


function shareFBonClick(){
    FB.ui({
        method: 'feed',
        link: 'https://www.facebook.com/atlantynespisuyut/',
        //caption: 'An example caption'
    }, function(response){
        // if (response === null) {
        if (rresponse && !response.error_code) {
            setCookiesShareTrue();
        } else {
            console.log('was not shared');
        }
    });
}




function setCookiesShareTrue() {
    document.cookie = "Share=true";
    console.log("Share=true");
}
