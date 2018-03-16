$(document).ready(function() {
    var logContainer = $('.log-container');
    var logItem = logContainer.find('.log-item');

    var reloadData = function() {
        var countItems = logContainer.find('.log-item').length;
        $.get('/stats/' + countItems, function(data) {
            var answer = $.parseJSON(data);
            answer.forEach(logText => {
                var newLogItem = logItem.clone();
                newLogItem.text(logText);
                logContainer.prepend(newLogItem);
            });
        });
    };

    reloadData();

    setInterval(function() {
        reloadData();
    }, 1000);
})