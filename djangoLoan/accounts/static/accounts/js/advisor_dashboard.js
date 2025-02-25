class UserManager {
    constructor(token, baseUrl) {
        this.token = token;
        this.baseUrl = baseUrl;
        console.log("UserManager initialisé");
        // Vérifier que le token est valide
        if (!token) {
            console.error("Token manquant");
            alert("Session expirée. Veuillez vous reconnecter.");
        }
    }

    loadUsers() {
        console.log("Chargement des utilisateurs...");
        fetch(`${this.baseUrl}/list`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        })
        .then(response => {
            console.log("Réponse liste: ", response.status);
            if (!response.ok) {
                throw new Error(`Erreur ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(users => {
            console.log("Utilisateurs chargés: ", users.length);
            const tbody = document.querySelector('#usersTable tbody');
            tbody.innerHTML = '';
            users.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user.email}</td>
                    <td>${user.first_name || ''}</td>
                    <td>${user.last_name || ''}</td>
                    <td>${user.is_staff ? 'Staff' : 'Client'}</td>
                    <td>
                        <button class="delete-btn" data-id="${user.id}">Supprimer</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
            
            // Ajouter handlers pour les boutons de suppression
            document.querySelectorAll('.delete-btn').forEach(btn => {
                btn.addEventListener('click', () => this.deleteUser(btn.dataset.id));
            });
        })
        .catch(error => {
            console.error("Erreur chargement utilisateurs: ", error);
            alert('Erreur lors du chargement des utilisateurs. Vérifiez la console.');
        });
    }

    deleteUser(userId) {
        if (confirm('Voulez-vous vraiment supprimer cet utilisateur ?')) {
            fetch(`${this.baseUrl}/user/${userId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            })
            .then(response => {
                console.log("Réponse suppression: ", response.status);
                if (response.ok) {
                    this.loadUsers();
                    alert('Utilisateur supprimé avec succès');
                } else {
                    alert(`Erreur lors de la suppression: ${response.status}`);
                }
            })
            .catch(error => {
                console.error("Erreur suppression: ", error);
                alert('Erreur lors de la suppression');
            });
        }
    }

    initCreateForm() {
        const form = document.getElementById('createUserForm');
        console.log("Formulaire trouvé: ", !!form);
        
        if (!form) return;
        
        form.addEventListener('submit', (e) => {
            console.log("Soumission du formulaire");
            e.preventDefault();
            
            const userData = {
                email: form.email.value,
                password: form.password.value,
                is_staff: false
            };
            
            console.log("Données utilisateur: ", userData);
            
            fetch(`${this.baseUrl}/create_user`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            })
            .then(response => {
                console.log("Réponse création: ", response.status);
                return response.text().then(text => {
                    return { 
                        ok: response.ok, 
                        status: response.status, 
                        body: text 
                    };
                });
            })
            .then(result => {
                console.log("Résultat: ", result);
                if (result.ok) {
                    form.reset();
                    this.loadUsers();
                    alert('Utilisateur créé avec succès');
                } else {
                    alert(`Erreur lors de la création: ${result.status} - ${result.body}`);
                }
            })
            .catch(error => {
                console.error("Exception: ", error);
                alert('Erreur lors de la création de l\'utilisateur');
            });
            
            // Empêcher la soumission normale du formulaire
            return false;
        });
    }

    init() {
        this.initCreateForm();
        this.loadUsers();
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    console.log("DOM chargé");
    window.userManager = new UserManager(window.API_TOKEN, window.API_BASE_URL);
    window.userManager.init();
});