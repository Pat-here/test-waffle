// Gofry Business System - Main JavaScript

// Globalne funkcje pomocnicze
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastBody = document.getElementById('toast-body');

    toastBody.textContent = message;
    toast.className = `toast ${type === 'success' ? 'bg-success' : 'bg-danger'}`;

    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('pl-PL', {
        style: 'currency',
        currency: 'PLN'
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('pl-PL');
}

function formatDateTime(dateString) {
    return new Date(dateString).toLocaleString('pl-PL');
}

// API helper functions
async function apiCall(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        showToast('Błąd połączenia z serwerem', 'error');
        throw error;
    }
}

// Inicjalizacja po załadowaniu strony
document.addEventListener('DOMContentLoaded', function() {
    // Ustawienie dzisiejszej daty w formularzach
    const today = new Date().toISOString().split('T')[0];
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (!input.value) {
            input.value = today;
        }
    });

    // Animacje fade-in dla kart
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100);
    });
});

// Funkcje do zarządzania loading state
function setLoading(element, isLoading) {
    if (isLoading) {
        element.disabled = true;
        element.innerHTML = '<span class="spinner"></span> Ładowanie...';
    } else {
        element.disabled = false;
        // Przywróć oryginalny tekst
    }
}

// Walidacja formularzy
function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// Export funkcji do innych skryptów
window.gofrySys = {
    showToast,
    formatCurrency,
    formatDate,
    formatDateTime,
    apiCall,
    setLoading,
    validateForm
};
