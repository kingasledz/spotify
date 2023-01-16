$('#date').datepicker({});

document.getElementById('confirm-button')
    .addEventListener('click', (ev) => {
        const date = document.getElementById('date-input').value;
        localStorage.setItem('date', date);
    })