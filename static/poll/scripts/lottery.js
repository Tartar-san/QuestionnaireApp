function hideUnknown(id) {
    $('#' + id + '_checkbox')[0].checked = false;
    $('#' + id + '_unknown').hide();
    $('#' + id + '_tail').show();
}

function toggleCoin(id) {
    $('#' + id + '_tail').toggle();
    $('#' + id + '_head').toggle();
}

function getCheckbox(id) {
    return $('#' + id + '_checkbox')[0];
}

function flipCoin(id, isHead) {
    var checkbox = getCheckbox(id);
    if (!isHead === checkbox.checked) {
        checkbox.checked = !checkbox.checked;
        toggleCoin(id);
    }
}

function getRandom(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}

function generateSequence() {
    for (var i = 1; i < 11; i++) {
        var id = 'coin' + i;
        if (!checkUnknown(id)) hideUnknown(id);
        getRandom(0, 2) === 0 ? flipCoin(id, false) : flipCoin(id, true);
    }
    $('#generate').prop('disabled', true).addClass("btn-disabled");
}

function setHandler(id) {
    $('#' + id + '_checkbox').on('change', function () {

        !checkUnknown(id) ? hideUnknown(id) : toggleCoin(id);

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
        if ($("#generate").length && !checkCoins()) return false;
        if (!$('#mainForm')[0].checkValidity())return false;
    });

});