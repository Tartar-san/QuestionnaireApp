function hideUnknown(id) {

    setHandler(id, toggleCoin);
}
function toggleCoin(id) {


}


function setHandler(id) {
    $('#' + id + '_checkbox').on('change', function () {

        if (!checkUnknown(id)) {
            $('#' + id + '_checkbox')[0].checked = false;
            $('#' + id + '_unknown').hide();
            $('#' + id + '_tail').show();
        } else {
            $('#' + id + '_tail').toggle();
            $('#' + id + '_head').toggle();
        }
    });
}

function checkUnknown(id) {
    return $('#' + id + '_unknown').css('display') === 'none';
}

function checkCoins() {
    for (var i = 1; i < 11; i++) {
        if (!checkUnknown('coin' + i)) return false;
    }
    return true;
}

$(document).ready(function () {
    for (var i = 1; i < 11; i++) {
        setHandler('coin' + i);
    }

    $('#mainForm').submit(function () {
        if (!checkCoins()) return false;

    });

});