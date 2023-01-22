$("#date").datepicker({
    startView: 3,
    endDate: new Date(),
}).on('changeDate', function (e) { 
    if (e.date.getFullYear() < 1959 || e.date >= Date.now()) {
        document.querySelector('.wrong-date').style.visibility = 'visible';
        document.getElementById('confirm-button').disabled = true;
    } else {
        document.querySelector('.wrong-date').style.visibility = '';
        document.getElementById('confirm-button').disabled = false;
    }
});
