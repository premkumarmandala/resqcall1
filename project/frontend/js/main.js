const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_URL = isLocalhost 
    ? `${window.location.protocol}//${window.location.hostname}:5000` 
    : 'https://resqcall.onrender.com'; // NOTE: Update this URL after deploying the backend to Render


// Auth Helpers
function getToken() {
    const t = localStorage.getItem('token');
    return (t && t !== 'undefined') ? t : null;
}

function getUser() {
    try {
        const u = localStorage.getItem('user');
        return (u && u !== 'undefined') ? JSON.parse(u) : {};
    } catch { return {}; }
}

function isLoggedIn() { return !!getToken(); }

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

function checkAuthRedirect() {
    if (!isLoggedIn()) {
        window.location.href = 'login.html';
    }
}

async function apiCall(endpoint, method = 'GET', data = null) {
    const headers = { 'Content-Type': 'application/json' };
    const token = getToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const config = { method, headers };
    if (data) config.body = JSON.stringify(data);

    try {
        const res = await fetch(`${API_URL}${endpoint}`, config);

        if (res.status === 401) {
            console.warn('Unauthorized. Redirecting...');
            if (window.location.pathname.indexOf('login.html') === -1) {
                logout();
            }
            return null;
        }

        let json = null;
        try {
            const text = await res.text();
            json = JSON.parse(text);
        } catch (e) {
            // Not a JSON response, likely an HTML 500 server error
            if (!res.ok) {
                return { error: true, message: `Server error (${res.status}): Please check backend logs.` };
            }
        }

        // If the backend returns a message but it's an error status
        if (!res.ok) {
            return { error: true, message: (json && json.message) ? json.message : 'Request failed' };
        }
        return json;
    } catch (err) {
        console.error('Network Error:', err);
        return { error: true, message: 'Network/CORS Error: Backend not reachable at ' + API_URL + '\\nThis usually means the backend is returning a 500 Error without CORS headers (e.g., Database connection failure) or not running.' };
    }
}

// UI Helpers
function setupSidebar() {
    const user = getUser();
    const sidebar = document.getElementById('sidebar');
    if (!sidebar) return;

    const sidebarHtml = `
        <div class="logo">
            <span style="font-size: 2rem;">🚑</span> ResQAdmin
        </div>
        <nav>
            <a href="dashboard.html" class="nav-link" id="nav-dash">📊 Dashboard</a>
            <a href="hospitals.html" class="nav-link" id="nav-hosp">🏥 Hospitals</a>
            <a href="ambulances.html" class="nav-link" id="nav-amb">🚑 Ambulances</a>
            <a href="emergencies.html" class="nav-link" id="nav-emg">🚨 Emergencies</a>
            <a href="users.html" class="nav-link" id="nav-users">👥 Users</a>
            <a href="call_logs.html" class="nav-link" id="nav-calls">📞 Call History</a>
        </nav>
        <div style="margin-top: auto;">
             <div style="padding: 1rem; border-top: 1px solid var(--border-color);">
                <small style="color: var(--text-secondary);">Logged in as:</small><br>
                <strong>${user.name || 'Admin'}</strong>
             </div>
            <button onclick="logout()" class="btn btn-danger" style="margin-top: 1rem; width: 100%;">Logout</button>
        </div>
    `;

    sidebar.innerHTML = sidebarHtml;

    // Highlight current page
    const path = window.location.pathname;
    if (path.includes('dashboard')) document.getElementById('nav-dash')?.classList.add('active');
    if (path.includes('hospitals')) document.getElementById('nav-hosp')?.classList.add('active');
    if (path.includes('ambulances')) document.getElementById('nav-amb')?.classList.add('active');
    if (path.includes('emergencies')) document.getElementById('nav-emg')?.classList.add('active');
    if (path.includes('users')) document.getElementById('nav-users')?.classList.add('active');
    if (path.includes('call_logs')) document.getElementById('nav-calls')?.classList.add('active');
}
