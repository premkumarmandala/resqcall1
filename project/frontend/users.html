<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>ResQ Admin | Users</title>
    <link rel="stylesheet" href="css/style.css">
</head>

<body>
    <div class="dashboard-layout">
        <aside class="sidebar" id="sidebar"></aside>

        <main class="main-content">
            <header style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
                <h1>User Management</h1>
                <button class="btn btn-primary" onclick="openUserModal()">+ Create User</button>
            </header>

            <div class="card">
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Role</th>
                                <th>Contact</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="userTable"></tbody>
                    </table>
                </div>
            </div>
        </main>
    </div>

    <!-- Create User Modal -->
    <div class="modal" id="userModal">
        <div class="modal-content">
            <h3>Create New User</h3>

            <div class="form-group">
                <label>Full Name</label>
                <input type="text" id="userName" class="form-input" required>
            </div>

            <div class="form-group">
                <label>Email</label>
                <input type="email" id="userEmail" class="form-input" required>
            </div>

            <div class="form-group">
                <label>Phone</label>
                <input type="text" id="userPhone" class="form-input" required>
            </div>

            <div class="form-group">
                <label>Role</label>
                <select id="userRole" class="form-input">
                    <option value="driver">Ambulance Driver</option>
                    <option value="hospital_admin">Hospital Admin</option>
                    <option value="admin">System Admin</option>
                </select>
            </div>

            <div class="form-group">
                <label>Password</label>
                <input type="password" id="userPass" class="form-input" required>
            </div>

            <div style="display: flex; gap: 1rem; margin-top: 1rem;">
                <button class="btn btn-primary" onclick="createUser()">Create Account</button>
                <button class="btn" onclick="closeModal('userModal')">Cancel</button>
            </div>
        </div>
    </div>

    <script src="js/main.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', async () => {
            checkAuthRedirect();
            setupSidebar();
            loadUsers();
        });

        async function loadUsers() {
            const users = await apiCall('/users');
            const tbody = document.getElementById('userTable');
            tbody.innerHTML = '';

            if (users) {
                users.forEach(u => {
                    const row = `
                        <tr>
                            <td style="font-weight: 500;">
                                ${u.name}
                                <div style="font-size: 0.75rem; color: var(--text-secondary);">${u.email}</div>
                            </td>
                            <td><span class="badge" style="background: var(--bg-color); border: 1px solid var(--border-color);">${u.role}</span></td>
                            <td>${u.phone}</td>
                            <td>
                                <span class="badge ${u.is_active ? 'badge-available' : 'badge-busy'}">
                                    ${u.is_active ? 'Active' : 'Disabled'}
                                </span>
                            </td>
                            <td>
                                <button class="btn" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="toggleUser(${u.id}, ${u.is_active})">
                                    ${u.is_active ? 'Disable' : 'Activate'}
                                </button>
                                <button class="btn" style="padding: 0.25rem 0.5rem; font-size: 0.75rem; background: var(--warning-yellow); margin-left: 0.5rem;" onclick="resetPass(${u.id})">
                                    Reset PW
                                </button>
                            </td>
                        </tr>
                    `;
                    tbody.innerHTML += row;
                });
            }
        }

        function openUserModal() { document.getElementById('userModal').classList.add('active'); }
        function closeModal(id) { document.getElementById(id).classList.remove('active'); }

        async function createUser() {
            const data = {
                name: document.getElementById('userName').value,
                email: document.getElementById('userEmail').value,
                phone: document.getElementById('userPhone').value,
                role: document.getElementById('userRole').value,
                password: document.getElementById('userPass').value
            };

            const res = await apiCall('/users/', 'POST', data);
            if (res && !res.error) {
                closeModal('userModal');
                loadUsers();
            } else {
                alert('Error creating user: ' + (res.message || 'Unknown'));
            }
        }

        async function toggleUser(id, currentStatus) {
            await apiCall(`/users/${id}/status`, 'PUT', { is_active: !currentStatus });
            loadUsers();
        }

        async function resetPass(id) {
            const p = prompt("Enter new password for this user:");
            if (p) {
                const res = await apiCall(`/users/${id}/password`, 'PUT', { password: p });
                if (res && !res.error) alert('Password changed.');
                else alert('Error: ' + (res ? res.message : 'Unknown'));
            }
        }
    </script>
</body>

</html>