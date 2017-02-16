/**
 * Created by D1mD1m on 2/8/2017.
 */




function setCookiesLikeTrue() {
    document.cookie = "Like=true";
    alert("");
}


function shareFBonClick(){
    FB.ui({
        method: 'feed',
        link: 'https://www.facebook.com/atlantynespisuyut/',
        //caption: 'An example caption'
    }, function(response){
        if (response === null) {
            console.log('was not shared');
        } else {
            setCookiesShareTrue();
        }
    });
}




function setCookiesShareTrue() {
    document.cookie = "Share=true";
    alert("shared");
}
