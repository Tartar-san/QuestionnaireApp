function setHandler(id) {
    $('#' + id + '_checkbox').on('change', function () {
            $('#' + id + '_tail').toggle();
            $('#' + id + '_head').toggle();
    });
}

$(document).ready(function () {
    for (var i = 1; i < 11; i++) {
        setHandler('coin' + i);
    }

});