// static/js/painel.js

document.addEventListener('DOMContentLoaded', () => {
    const addContentForm = document.getElementById('addContentForm');
    const contentsTableBody = document.getElementById('contentsTableBody');
    const editModal = document.getElementById('editModal');
    const closeButton = document.querySelector('.close-button');
    const editContentForm = document.getElementById('editContentForm');
    const editIdInput = document.getElementById('edit-id');
    const editTitleInput = document.getElementById('edit-title');
    const editDescriptionInput = document.getElementById('edit-description');
    const editCategoryInput = document.getElementById('edit-category');
    const editLineInput = document.getElementById('edit-line');         
    const editImagemInput = document.getElementById('edit-imagem');   
    const currentImageName = document.getElementById('currentImageName');
    const removeImageCheckbox = document.getElementById('remove-image');

    const addMessageArea = document.getElementById('addMessageArea');
    const listMessageArea = document.getElementById('listMessageArea');
    const editMessageArea = document.getElementById('editMessageArea');

    function showMessage(area, message, type = 'success') {
        area.textContent = message;
        area.className = `message-area ${type}`;
        setTimeout(() => {
            area.textContent = '';
            area.className = 'message-area';
        }, 3000);
    }

    async function fetchContents() {
        try {
            const response = await fetch('/api/content');
            if (!response.ok) {
                throw new Error('Falha ao buscar conteúdo.');
            }
            const contents = await response.json();
            renderContents(contents);
        } catch (error) {
            console.error('Erro ao buscar conteúdos:', error);
            showMessage(listMessageArea, 'Erro ao carregar conteúdo: ' + error.message, 'error');
        }
    }

    function renderContents(contents) {
        contentsTableBody.innerHTML = '';
        if (contents.length === 0) {
            contentsTableBody.innerHTML = '<tr><td colspan="7">Nenhum conteúdo cadastrado.</td></tr>';
            return;
        }

        contents.forEach(item => {
            const row = contentsTableBody.insertRow();
            row.dataset.id = item.id;

            row.insertCell(0).textContent = item.id;
            row.insertCell(1).textContent = item.title;
            row.insertCell(2).textContent = item.description;
            row.insertCell(3).textContent = item.category || 'N/A'; // NOVO
            row.insertCell(4).textContent = item.line || 'N/A';     // NOVO

            const imageCell = row.insertCell(5);
            if (item.image_filename) {
                const img = document.createElement('img');
                img.src = `/static/uploads/${item.image_filename}`;
                img.alt = item.title;
                img.style.maxWidth = '80px';
                img.style.maxHeight = '80px';
                imageCell.appendChild(img);
            } else {
                imageCell.textContent = 'N/A';
            }

            const actionsCell = row.insertCell(6);
            const editBtn = document.createElement('button');
            editBtn.textContent = 'Editar';
            editBtn.classList.add('edit-btn');
            editBtn.addEventListener('click', () => openEditModal(item.id));

            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Deletar';
            deleteBtn.classList.add('delete-btn');
            deleteBtn.addEventListener('click', () => deleteContent(item.id));

            actionsCell.appendChild(editBtn);
            actionsCell.appendChild(deleteBtn);
        });
    }

    addContentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(addContentForm);

        try {
            const response = await fetch('/api/content', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            if (response.ok) {
                showMessage(addMessageArea, data.message || 'Conteúdo adicionado com sucesso!');
                addContentForm.reset();
                fetchContents();
            } else {
                throw new Error(data.message || 'Erro ao adicionar conteúdo.');
            }
        } catch (error) {
            console.error('Erro ao adicionar conteúdo:', error);
            showMessage(addMessageArea, error.message, 'error');
        }
    });

    async function openEditModal(id) {
        try {
            const response = await fetch(`/api/content/${id}`);
            if (!response.ok) {
                throw new Error('Falha ao buscar conteúdo para edição.');
            }
            const item = await response.json();

            editIdInput.value = item.id;
            editTitleInput.value = item.title;
            editDescriptionInput.value = item.description;
            editCategoryInput.value = item.category || ''; 
            editLineInput.value = item.line || '';        

            editImagemInput.value = ''; // Limpa o input de arquivo
            removeImageCheckbox.checked = false;

            if (item.image_filename) {
                currentImageName.textContent = `Imagem atual: ${item.image_filename}`;
            } else {
                currentImageName.textContent = 'Nenhuma imagem associada.';
            }

            editModal.style.display = 'block';
        } catch (error) {
            console.error('Erro ao abrir modal de edição:', error);
            showMessage(listMessageArea, 'Erro ao carregar conteúdo para edição: ' + error.message, 'error');
        }
    }

    editContentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const contentId = editIdInput.value;
        const formData = new FormData(editContentForm);

        try {
            const response = await fetch(`/api/content/${contentId}`, {
                method: 'PUT',
                body: formData
            });
            const data = await response.json();
            if (response.ok) {
                showMessage(editMessageArea, data.message || 'Conteúdo atualizado com sucesso!');
                fetchContents();
                setTimeout(() => {
                    editModal.style.display = 'none';
                    editMessageArea.textContent = '';
                }, 1500);
            } else {
                throw new Error(data.message || 'Erro ao atualizar conteúdo.');
            }
        } catch (error) {
            console.error('Erro ao atualizar conteúdo:', error);
            showMessage(editMessageArea, error.message, 'error');
        }
    });

    closeButton.addEventListener('click', () => {
        editModal.style.display = 'none';
        editMessageArea.textContent = '';
    });

    window.addEventListener('click', (event) => {
        if (event.target == editModal) {
            editModal.style.display = 'none';
            editMessageArea.textContent = '';
        }
    });

    async function deleteContent(id) {
        if (!confirm('Tem certeza que deseja deletar este conteúdo?')) {
            return;
        }
        try {
            const response = await fetch(`/api/content/${id}`, {
                method: 'DELETE'
            });
            if (response.ok) {
                showMessage(listMessageArea, 'Conteúdo deletado com sucesso!', 'success');
                fetchContents();
            } else {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Falha ao deletar conteúdo.');
            }
        } catch (error) {
            console.error('Erro ao deletar conteúdo:', error);
            showMessage(listMessageArea, error.message, 'error');
        }
    }

    fetchContents();
});
