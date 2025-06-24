// Gofry Business System - Notes JavaScript

let editingNoteId = null;

// Ładowanie notatek
async function loadNotes() {
    try {
        const notes = await gofrySys.apiCall('/api/notes');
        displayNotes(notes);
    } catch (error) {
        console.error('Błąd ładowania notatek:', error);
    }
}

// Wyświetlanie notatek
function displayNotes(notes) {
    const container = document.getElementById('notesContainer');
    container.innerHTML = '';

    if (notes.length === 0) {
        container.innerHTML = `
            <div class="col-12">
                <div class="text-center py-5">
                    <i class="fas fa-sticky-note fa-3x text-muted mb-3"></i>
                    <h5 class="text-muted">Brak notatek</h5>
                    <p class="text-muted">Dodaj pierwszą notatkę klikając przycisk "Nowa notatka"</p>
                </div>
            </div>
        `;
        return;
    }

    notes.forEach(note => {
        const priorityClass = `priority-${note.priority}`;
        const priorityText = {
            'low': 'Niski',
            'medium': 'Średni',
            'high': 'Wysoki'
        }[note.priority];

        const noteCard = `
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h6 class="mb-0">${note.title}</h6>
                        <span class="badge ${priorityClass}">${priorityText}</span>
                    </div>
                    <div class="card-body">
                        <p class="card-text">${note.content}</p>
                        <small class="text-muted">
                            Utworzono: ${gofrySys.formatDateTime(note.created_at)}<br>
                            ${note.updated_at !== note.created_at ? 'Edytowano: ' + gofrySys.formatDateTime(note.updated_at) : ''}
                        </small>
                    </div>
                    <div class="card-footer d-flex justify-content-between">
                        <button class="btn btn-outline-primary btn-sm" onclick="editNote(${note.id})">
                            <i class="fas fa-edit"></i> Edytuj
                        </button>
                        <button class="btn btn-outline-danger btn-sm" onclick="deleteNote(${note.id})">
                            <i class="fas fa-trash"></i> Usuń
                        </button>
                    </div>
                </div>
            </div>
        `;
        container.innerHTML += noteCard;
    });
}

// Zapisywanie notatki
async function saveNote() {
    if (!gofrySys.validateForm('noteForm')) {
        gofrySys.showToast('Wypełnij wszystkie wymagane pola', 'error');
        return;
    }

    const data = {
        title: document.getElementById('noteTitle').value,
        content: document.getElementById('noteContent').value,
        priority: document.getElementById('notePriority').value
    };

    try {
        if (editingNoteId) {
            await gofrySys.apiCall(`/api/notes/${editingNoteId}`, 'PUT', data);
            gofrySys.showToast('Notatka została zaktualizowana');
        } else {
            await gofrySys.apiCall('/api/notes', 'POST', data);
            gofrySys.showToast('Notatka została dodana');
        }

        clearNoteForm();
        bootstrap.Modal.getInstance(document.getElementById('noteModal')).hide();
        loadNotes();
    } catch (error) {
        gofrySys.showToast('Błąd podczas zapisywania notatki', 'error');
    }
}

// Edycja notatki
async function editNote(id) {
    try {
        const notes = await gofrySys.apiCall('/api/notes');
        const note = notes.find(n => n.id === id);

        if (note) {
            editingNoteId = id;
            document.getElementById('noteTitle').value = note.title;
            document.getElementById('noteContent').value = note.content;
            document.getElementById('notePriority').value = note.priority;
            document.getElementById('noteModalTitle').textContent = 'Edytuj notatkę';

            new bootstrap.Modal(document.getElementById('noteModal')).show();
        }
    } catch (error) {
        gofrySys.showToast('Błąd podczas ładowania notatki', 'error');
    }
}

// Usuwanie notatki
async function deleteNote(id) {
    if (confirm('Czy na pewno chcesz usunąć tę notatkę?')) {
        try {
            await gofrySys.apiCall(`/api/notes/${id}`, 'DELETE');
            gofrySys.showToast('Notatka została usunięta');
            loadNotes();
        } catch (error) {
            gofrySys.showToast('Błąd podczas usuwania notatki', 'error');
        }
    }
}

// Czyszczenie formularza
function clearNoteForm() {
    editingNoteId = null;
    document.getElementById('noteForm').reset();
    document.getElementById('noteModalTitle').textContent = 'Nowa notatka';
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    loadNotes();

    // Resetowanie formularza przy zamykaniu modala
    document.getElementById('noteModal').addEventListener('hidden.bs.modal', clearNoteForm);
});
