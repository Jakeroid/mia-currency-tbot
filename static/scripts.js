$(document).ready(function() {
    var logContainer = $('.log-container');
    var logItem = logContainer.find('.log-item');
    setInterval(function() {
        $.get('/stats', function(data) {
            var answer = $.parseJSON(data);
            answer.forEach(logText => {
                var newLogItem = logItem.clone();
                newLogItem.text(logText);
                logContainer.append(newLogItem);
            });
        });
    }, 2000);
})