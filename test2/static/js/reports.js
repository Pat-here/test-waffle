// Gofry Business System - Reports JavaScript

// Ładowanie raportów
async function loadReports() {
    try {
        const reports = await gofrySys.apiCall('/api/reports');
        displayReports(reports);
        loadMonthlySummary();
    } catch (error) {
        console.error('Błąd ładowania raportów:', error);
    }
}

// Wyświetlanie raportów
function displayReports(reports) {
    const tbody = document.getElementById('reportsTableBody');
    tbody.innerHTML = '';

    if (reports.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center py-4">
                    <i class="fas fa-chart-bar fa-2x text-muted mb-2"></i>
                    <p class="text-muted mb-0">Brak raportów dziennych</p>
                </td>
            </tr>
        `;
        return;
    }

    reports.forEach(report => {
        const profitClass = report.profit >= 0 ? 'text-success' : 'text-danger';
        const weather = report.weather ? report.weather : '-';

        const row = `
            <tr>
                <td><strong>${gofrySys.formatDate(report.report_date)}</strong></td>
                <td><strong class="text-success">${gofrySys.formatCurrency(report.revenue)}</strong></td>
                <td><strong class="text-danger">${gofrySys.formatCurrency(report.costs)}</strong></td>
                <td><strong class="${profitClass}">${gofrySys.formatCurrency(report.profit)}</strong></td>
                <td><span class="badge bg-info">${report.gofry_sold}</span></td>
                <td>${weather}</td>
                <td>
                    <button class="btn btn-outline-primary btn-sm" onclick="editReport(${report.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-outline-danger btn-sm" onclick="deleteReport(${report.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

// Ładowanie podsumowania miesięcznego
async function loadMonthlySummary() {
    const month = document.getElementById('monthSelect').value;
    const year = new Date().getFullYear();

    try {
        const summary = await gofrySys.apiCall(`/api/monthly-summary/${year}/${month}`);

        document.getElementById('monthlyRevenue').textContent = gofrySys.formatCurrency(summary.total_revenue);
        document.getElementById('monthlyCosts').textContent = gofrySys.formatCurrency(summary.total_costs);
        document.getElementById('monthlyProfit').textContent = gofrySys.formatCurrency(summary.total_profit);
        document.getElementById('monthlyGofry').textContent = summary.total_gofry;
        document.getElementById('workingDaysMonth').textContent = summary.working_days;
        document.getElementById('avgDailyRevenue').textContent = gofrySys.formatCurrency(summary.avg_daily_revenue);
    } catch (error) {
        console.error('Błąd ładowania podsumowania miesięcznego:', error);
    }
}

// Zapisywanie raportu
async function saveReport() {
    if (!gofrySys.validateForm('reportForm')) {
        gofrySys.showToast('Wypełnij wszystkie wymagane pola', 'error');
        return;
    }

    const data = {
        report_date: document.getElementById('reportDate').value,
        revenue: parseFloat(document.getElementById('revenue').value),
        costs: parseFloat(document.getElementById('costs').value),
        gofry_sold: parseInt(document.getElementById('gofrySold').value),
        weather: document.getElementById('weather').value,
        notes: document.getElementById('reportNotes').value
    };

    try {
        await gofrySys.apiCall('/api/reports', 'POST', data);
        gofrySys.showToast('Raport został zapisany');
        clearReportForm();
        bootstrap.Modal.getInstance(document.getElementById('reportModal')).hide();
        loadReports();
    } catch (error) {
        gofrySys.showToast('Błąd podczas zapisywania raportu', 'error');
    }
}

// Edycja raportu
async function editReport(id) {
    try {
        const reports = await gofrySys.apiCall('/api/reports');
        const report = reports.find(r => r.id === id);

        if (report) {
            document.getElementById('reportDate').value = report.report_date;
            document.getElementById('revenue').value = report.revenue;
            document.getElementById('costs').value = report.costs;
            document.getElementById('gofrySold').value = report.gofry_sold;
            document.getElementById('weather').value = report.weather || '';
            document.getElementById('reportNotes').value = report.notes || '';

            new bootstrap.Modal(document.getElementById('reportModal')).show();
        }
    } catch (error) {
        gofrySys.showToast('Błąd podczas ładowania raportu', 'error');
    }
}

// Usuwanie raportu
async function deleteReport(id) {
    if (confirm('Czy na pewno chcesz usunąć ten raport?')) {
        try {
            await gofrySys.apiCall(`/api/reports/${id}`, 'DELETE');
            gofrySys.showToast('Raport został usunięty');
            loadReports();
        } catch (error) {
            gofrySys.showToast('Błąd podczas usuwania raportu', 'error');
        }
    }
}

// Czyszczenie formularza
function clearReportForm() {
    document.getElementById('reportForm').reset();
    // Ustaw dzisiejszą datę
    document.getElementById('reportDate').value = new Date().toISOString().split('T')[0];
}

// Automatyczne obliczanie zysku
function calculateProfit() {
    const revenue = parseFloat(document.getElementById('revenue').value) || 0;
    const costs = parseFloat(document.getElementById('costs').value) || 0;
    const profit = revenue - costs;

    // Można dodać element do wyświetlania kalkulowanego zysku
    console.log('Kalkulowany zysk:', profit);
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    loadReports();

    // Resetowanie formularza przy zamykaniu modala
    document.getElementById('reportModal').addEventListener('hidden.bs.modal', clearReportForm);

    // Automatyczne obliczanie zysku przy zmianie wartości
    document.getElementById('revenue').addEventListener('input', calculateProfit);
    document.getElementById('costs').addEventListener('input', calculateProfit);
});
