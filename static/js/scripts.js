document.addEventListener('DOMContentLoaded', function() {
    const reservedDatesElement = document.getElementById('reserved-dates');
    const reservedDates = JSON.parse(reservedDatesElement.textContent);

    function disableReservedDates(date) {
        const formattedDate = date.toISOString().split('T')[0];
        return reservedDates.includes(formattedDate);
    }

    const today = new Date().toISOString().split('T')[0];

    flatpickr("#id_rental_date", {
        mode: "range",
        disable: [disableReservedDates],
        minDate: "today",
        onChange: function(selectedDates, dateStr, instance) {
            const rentalDateInput = document.getElementById('id_rental_date');
            const returnDateInput = document.getElementById('id_return_date');
            if (selectedDates.length === 2) {
                const [startDate, endDate] = selectedDates;
                rentalDateInput.value = startDate.toLocaleDateString('lt');
                returnDateInput.value = endDate.toLocaleDateString('lt');
            }
        }
    });

    flatpickr("#id_return_date", {
        disable: [disableReservedDates],
        minDate: "today"
    });
});
