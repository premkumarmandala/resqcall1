:root {
    --primary-blue: #0ea5e9;
    --primary-dark-blue: #0369a1;
    --emergency-red: #ef4444;
    --emergency-dark-red: #b91c1c;
    --success-green: #22c55e;
    --warning-yellow: #eab308;
    
    --bg-color: #f8fafc;
    --surface-color: #ffffff;
    --text-primary: #1e293b;
    --text-secondary: #64748b;
    --border-color: #e2e8f0;
    
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    
    --radius: 0.75rem;
    --font-inter: 'Inter', system-ui, sans-serif;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: var(--font-inter);
    background-color: var(--bg-color);
    color: var(--text-primary);
    line-height: 1.5;
}

h1, h2, h3, h4, h5, h6 {
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

a {
    text-decoration: none;
    color: var(--primary-blue);
    transition: color 0.2s;
}

button {
    cursor: pointer;
    font-family: inherit;
    border: none;
}

/* Layout */
.container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 1rem;
}

.dashboard-layout {
    display: flex;
    min-height: 100vh;
}

.sidebar {
    width: 280px;
    background-color: var(--surface-color);
    border-right: 1px solid var(--border-color);
    padding: 1.5rem;
    position: sticky;
    top: 0;
    height: 100vh;
    display: flex;
    flex-direction: column;
}

.main-content {
    flex: 1;
    padding: 2rem;
    overflow-y: auto;
}

/* Auth Pages */
.auth-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, var(--bg-color) 0%, #e0f2fe 100%);
}

.auth-card {
    background: var(--surface-color);
    padding: 2.5rem;
    border-radius: var(--radius);
    box-shadow: var(--shadow-lg);
    width: 100%;
    max-width: 400px;
}

.form-group {
    margin-bottom: 1.25rem;
}

.form-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    font-size: 0.875rem;
    color: var(--text-secondary);
}

.form-input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    font-size: 1rem;
    transition: all 0.2s;
}

.form-input:focus {
    outline: none;
    border-color: var(--primary-blue);
    box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1);
}

.btn {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    padding: 0.75rem 1.5rem;
    border-radius: var(--radius);
    font-weight: 600;
    font-size: 0.875rem;
    transition: all 0.2s;
    width: 100%;
}

.btn-primary {
    background-color: var(--primary-blue);
    color: white;
}

.btn-primary:hover {
    background-color: var(--primary-dark-blue);
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

.btn-danger {
    background-color: var(--emergency-red);
    color: white;
}
.btn-danger:hover {
    background-color: var(--emergency-dark-red);
}

/* Sidebar */
.nav-link {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    color: var(--text-secondary);
    border-radius: var(--radius);
    margin-bottom: 0.5rem;
    font-weight: 500;
}

.nav-link.active, .nav-link:hover {
    background-color: #f0f9ff;
    color: var(--primary-blue);
}

.logo {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--emergency-red);
    margin-bottom: 2rem;
}

/* Cards */
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.card {
    background: var(--surface-color);
    padding: 1.5rem;
    border-radius: var(--radius);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-color);
}

.stat-value {
    font-size: 2rem;
    font-weight: 800;
    margin: 0.5rem 0;
}

.stat-label {
    color: var(--text-secondary);
    font-size: 0.875rem;
}

/* Tables */
.table-container {
    background: var(--surface-color);
    border-radius: var(--radius);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-color);
    overflow: hidden;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th {
    background-color: #f8fafc;
    padding: 1rem;
    text-align: left;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
    border-bottom: 1px solid var(--border-color);
}

td {
    padding: 1rem;
    border-bottom: 1px solid var(--border-color);
}

tr:last-child td {
    border-bottom: none;
}

/* Badges */
.badge {
    padding: 0.25rem 0.5rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-available { background: #dcfce7; color: #166534; }
.badge-busy { background: #fee2e2; color: #991b1b; }
.badge-offline { background: #f1f5f9; color: #475569; }

/* Modal */
.modal {
    display: none;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.5);
    align-items: center;
    justify-content: center;
    z-index: 50;
    backdrop-filter: blur(4px);
}
.modal.active { display: flex; }
.modal-content {
    background: white;
    padding: 2rem;
    border-radius: var(--radius);
    width: 100%;
    max-width: 500px;
    box-shadow: var(--shadow-lg);
}
