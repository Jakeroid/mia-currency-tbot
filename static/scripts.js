$(document).ready(function() {
    var logContainer = $('.log-container');
    var logItem = logContainer.find('.log-item');
    setInterval(function() {
        console.log('ss');
        $.get('/stats', function(answer) {
            answer.forEach(logText => {
                var newLogItem = logItem.clone();
                newLogItem.text(logText);
                logContainer.append(newLogItem);
            });
        });
    }, 2000);
})