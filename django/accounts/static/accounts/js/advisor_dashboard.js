class UserManager {
    constructor(token, baseUrl) {
        this.token = token;
        this.baseUrl = baseUrl;
    }

    loadUsers() {
        fetch(`${this.baseUrl}/users/list`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        })
        .then(response => response.json())
        .then(users => {
            const tbody = document.querySelector('#usersTable tbody');
            tbody.innerHTML = '';
            users.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                    <td>${user.role}</td>
                    <td>
                        <button onclick="userManager.deleteUser(${user.id})">Supprimer</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => alert('Erreur lors du chargement des utilisateurs'));
    }

    deleteUser(userId) {
        if (confirm('Voulez-vous vraiment supprimer cet utilisateur ?')) {
            fetch(`${this.baseUrl}/users/${userId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            })
            .then(response => {
                if (response.ok) {
                    this.loadUsers();
                    alert('Utilisateur supprimé avec succès');
                } else {
                    alert('Erreur lors de la suppression');
                }
            })
            .catch(error => alert('Erreur lors de la suppression'));
        }
    }

    initCreateForm() {
        document.getElementById('createUserForm').addEventListener('submit', (e) => {
            e.preventDefault();
            
            const form = e.target;
            const userData = {
                username: form.username.value,
                email: form.email.value,
                password: form.password.value
            };

            fetch(`${this.baseUrl}/users`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            })
            .then(response => {
                if (response.ok) {
                    form.reset();
                    this.loadUsers();
                    alert('Utilisateur créé avec succès');
                } else {
                    alert('Erreur lors de la création de l\'utilisateur');
                }
            })
            .catch(error => alert('Erreur lors de la création de l\'utilisateur'));
        });
    }

    init() {
        this.initCreateForm();
        this.loadUsers();
    }
}

createUser(userData)
 {
    fetch(`${this.baseUrl}/users`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => {
        if (response.ok) {
            this.loadUsers();
            alert('Utilisateur créé avec succès');
        } else {
            alert('Erreur lors de la création de l\'utilisateur');
        }
    })
    .catch(error => alert('Erreur lors de la création de l\'utilisateur'));
}

document.addEventListener('DOMContentLoaded', (event) => {
    const userManager = new UserManager('{{ request.session.token }}', 'http://127.0.0.1:8000');
    userManager.init();
});