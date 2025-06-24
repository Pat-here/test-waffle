// Gofry Business System - Work Hours JavaScript

// Ładowanie czasu pracy
async function loadWorkHours() {
    try {
        const workHours = await gofrySys.apiCall('/api/work-hours');
        displayWorkHours(workHours);
        updateWorkHoursStats(workHours);
    } catch (error) {
        console.error('Błąd ładowania czasu pracy:', error);
    }
}

// Wyświetlanie czasu pracy
function displayWorkHours(workHours) {
    const tbody = document.getElementById('workHoursTableBody');
    tbody.innerHTML = '';

    if (workHours.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="9" class="text-center py-4">
                    <i class="fas fa-clock fa-2x text-muted mb-2"></i>
                    <p class="text-muted mb-0">Brak wpisów czasu pracy</p>
                </td>
            </tr>
        `;
        return;
    }

    workHours.forEach(wh => {
        const row = `
            <tr>
                <td><strong>${wh.employee_name}</strong></td>
                <td>${gofrySys.formatDate(wh.work_date)}</td>
                <td>${wh.start_time}</td>
                <td>${wh.end_time}</td>
                <td>${wh.break_minutes} min</td>
                <td><strong>${wh.total_hours}h</strong></td>
                <td>${gofrySys.formatCurrency(wh.hourly_rate)}</td>
                <td><strong>${gofrySys.formatCurrency(wh.total_pay)}</strong></td>
                <td>
                    <button class="btn btn-outline-danger btn-sm" onclick="deleteWorkHour(${wh.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

// Aktualizacja statystyk czasu pracy
function updateWorkHoursStats(workHours) {
    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();

    const thisMonthHours = workHours.filter(wh => {
        const workDate = new Date(wh.work_date);
        return workDate.getMonth() === currentMonth && workDate.getFullYear() === currentYear;
    });

    const totalHours = thisMonthHours.reduce((sum, wh) => sum + wh.total_hours, 0);
    const totalPay = thisMonthHours.reduce((sum, wh) => sum + wh.total_pay, 0);
    const workingDays = new Set(thisMonthHours.map(wh => wh.work_date)).size;
    const avgHourlyRate = thisMonthHours.length > 0 ? 
        thisMonthHours.reduce((sum, wh) => sum + wh.hourly_rate, 0) / thisMonthHours.length : 0;

    document.getElementById('totalHoursThisMonth').textContent = totalHours.toFixed(1);
    document.getElementById('totalPayThisMonth').textContent = gofrySys.formatCurrency(totalPay);
    document.getElementById('avgHourlyRate').textContent = gofrySys.formatCurrency(avgHourlyRate);
    document.getElementById('workingDays').textContent = workingDays;
}

// Zapisywanie czasu pracy
async function saveWorkHour() {
    if (!gofrySys.validateForm('workHourForm')) {
        gofrySys.showToast('Wypełnij wszystkie wymagane pola', 'error');
        return;
    }

    const data = {
        employee_name: document.getElementById('employeeName').value,
        work_date: document.getElementById('workDate').value,
        start_time: document.getElementById('startTime').value,
        end_time: document.getElementById('endTime').value,
        break_minutes: parseInt(document.getElementById('breakMinutes').value) || 0,
        hourly_rate: parseFloat(document.getElementById('hourlyRate').value),
        notes: document.getElementById('workNotes').value
    };

    try {
        await gofrySys.apiCall('/api/work-hours', 'POST', data);
        gofrySys.showToast('Czas pracy został zapisany');
        clearWorkHourForm();
        bootstrap.Modal.getInstance(document.getElementById('workHourModal')).hide();
        loadWorkHours();
    } catch (error) {
        gofrySys.showToast('Błąd podczas zapisywania czasu pracy', 'error');
    }
}

// Usuwanie wpisu czasu pracy
async function deleteWorkHour(id) {
    if (confirm('Czy na pewno chcesz usunąć ten wpis czasu pracy?')) {
        try {
            await gofrySys.apiCall(`/api/work-hours/${id}`, 'DELETE');
            gofrySys.showToast('Wpis czasu pracy został usunięty');
            loadWorkHours();
        } catch (error) {
            gofrySys.showToast('Błąd podczas usuwania wpisu', 'error');
        }
    }
}

// Czyszczenie formularza
function clearWorkHourForm() {
    document.getElementById('workHourForm').reset();
    document.getElementById('hourlyRate').value = '20';
    document.getElementById('breakMinutes').value = '0';
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    loadWorkHours();

    // Resetowanie formularza przy zamykaniu modala
    document.getElementById('workHourModal').addEventListener('hidden.bs.modal', clearWorkHourForm);
});
