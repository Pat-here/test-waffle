// Gofry Business System - Orders JavaScript

// Ładowanie zamówień
async function loadOrders() {
    try {
        const orders = await gofrySys.apiCall('/api/orders');
        displayOrders(orders);
    } catch (error) {
        console.error('Błąd ładowania zamówień:', error);
    }
}

// Wyświetlanie zamówień
function displayOrders(orders) {
    const tbody = document.getElementById('ordersTableBody');
    tbody.innerHTML = '';

    if (orders.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center py-4">
                    <i class="fas fa-shopping-cart fa-2x text-muted mb-2"></i>
                    <p class="text-muted mb-0">Brak zamówień</p>
                </td>
            </tr>
        `;
        return;
    }

    orders.forEach(order => {
        const statusClass = `status-${order.status}`;
        const statusText = {
            'pending': 'Oczekujące',
            'ordered': 'Zamówione',
            'delivered': 'Dostarczone'
        }[order.status];

        const row = `
            <tr>
                <td>${gofrySys.formatDate(order.order_date)}</td>
                <td>${order.supplier}</td>
                <td><span class="badge ${statusClass}">${statusText}</span></td>
                <td>${order.delivery_date ? gofrySys.formatDate(order.delivery_date) : '-'}</td>
                <td><span class="badge bg-info">${order.items_count} poz.</span></td>
                <td><strong>${gofrySys.formatCurrency(order.total_cost)}</strong></td>
                <td>
                    <button class="btn btn-outline-primary btn-sm" onclick="updateOrderStatus(${order.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-outline-danger btn-sm" onclick="deleteOrder(${order.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

// Zapisywanie zamówienia
async function saveOrder() {
    if (!gofrySys.validateForm('orderForm')) {
        gofrySys.showToast('Wypełnij wszystkie wymagane pola', 'error');
        return;
    }

    const items = [];
    const orderItems = document.querySelectorAll('.order-item');

    orderItems.forEach(item => {
        const name = item.querySelector('.item-name').value;
        const quantity = parseFloat(item.querySelector('.item-quantity').value);
        const unit = item.querySelector('.item-unit').value;
        const price = parseFloat(item.querySelector('.item-price').value);

        if (name && quantity && price) {
            items.push({
                item_name: name,
                quantity: quantity,
                unit: unit,
                unit_price: price
            });
        }
    });

    if (items.length === 0) {
        gofrySys.showToast('Dodaj przynajmniej jedną pozycję do zamówienia', 'error');
        return;
    }

    const data = {
        supplier: document.getElementById('orderSupplier').value,
        order_date: document.getElementById('orderDate').value,
        delivery_date: document.getElementById('deliveryDate').value,
        notes: document.getElementById('orderNotes').value,
        items: items
    };

    try {
        await gofrySys.apiCall('/api/orders', 'POST', data);
        gofrySys.showToast('Zamówienie zostało dodane');
        clearOrderForm();
        bootstrap.Modal.getInstance(document.getElementById('orderModal')).hide();
        loadOrders();
    } catch (error) {
        gofrySys.showToast('Błąd podczas zapisywania zamówienia', 'error');
    }
}

// Dodawanie pozycji zamówienia
function addOrderItem() {
    const container = document.getElementById('orderItems');
    const newItem = document.createElement('div');
    newItem.className = 'order-item border p-3 mb-2';
    newItem.innerHTML = `
        <div class="row">
            <div class="col-md-4">
                <input type="text" class="form-control item-name" placeholder="Nazwa produktu" required>
            </div>
            <div class="col-md-2">
                <input type="number" class="form-control item-quantity" placeholder="Ilość" step="0.1" required>
            </div>
            <div class="col-md-2">
                <select class="form-select item-unit">
                    <option value="szt">szt</option>
                    <option value="kg">kg</option>
                    <option value="l">l</option>
                    <option value="op">op</option>
                </select>
            </div>
            <div class="col-md-2">
                <input type="number" class="form-control item-price" placeholder="Cena" step="0.01" required>
            </div>
            <div class="col-md-2">
                <button type="button" class="btn btn-danger btn-sm w-100" onclick="removeOrderItem(this)">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `;
    container.appendChild(newItem);
}

// Usuwanie pozycji zamówienia
function removeOrderItem(button) {
    const orderItems = document.querySelectorAll('.order-item');
    if (orderItems.length > 1) {
        button.closest('.order-item').remove();
    } else {
        gofrySys.showToast('Zamówienie musi mieć przynajmniej jedną pozycję', 'error');
    }
}

// Aktualizacja statusu zamówienia
async function updateOrderStatus(id) {
    const newStatus = prompt('Nowy status (pending/ordered/delivered):');
    if (newStatus && ['pending', 'ordered', 'delivered'].includes(newStatus)) {
        try {
            await gofrySys.apiCall(`/api/orders/${id}`, 'PUT', { status: newStatus });
            gofrySys.showToast('Status zamówienia został zaktualizowany');
            loadOrders();
        } catch (error) {
            gofrySys.showToast('Błąd podczas aktualizacji statusu', 'error');
        }
    }
}

// Usuwanie zamówienia
async function deleteOrder(id) {
    if (confirm('Czy na pewno chcesz usunąć to zamówienie?')) {
        try {
            await gofrySys.apiCall(`/api/orders/${id}`, 'DELETE');
            gofrySys.showToast('Zamówienie zostało usunięte');
            loadOrders();
        } catch (error) {
            gofrySys.showToast('Błąd podczas usuwania zamówienia', 'error');
        }
    }
}

// Czyszczenie formularza
function clearOrderForm() {
    document.getElementById('orderForm').reset();

    // Zostaw tylko jedną pozycję zamówienia
    const container = document.getElementById('orderItems');
    const items = container.querySelectorAll('.order-item');
    for (let i = 1; i < items.length; i++) {
        items[i].remove();
    }

    // Wyczyść pierwszą pozycję
    const firstItem = container.querySelector('.order-item');
    firstItem.querySelectorAll('input').forEach(input => input.value = '');
    firstItem.querySelector('select').selectedIndex = 0;
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    loadOrders();

    // Resetowanie formularza przy zamykaniu modala
    document.getElementById('orderModal').addEventListener('hidden.bs.modal', clearOrderForm);
});
