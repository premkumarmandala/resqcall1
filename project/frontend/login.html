<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ResQ Admin | Login</title>
    <link rel="stylesheet" href="css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        .tab-btn {
            background: none;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 600;
            color: var(--text-secondary);
            cursor: pointer;
            border-bottom: 2px solid transparent;
        }

        .tab-btn.active {
            color: var(--primary-blue);
            border-bottom-color: var(--primary-blue);
        }
    </style>
</head>

<body>
    <div class="auth-container">
        <div class="auth-card">
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🚑</div>
                <h1 style="color: var(--text-primary)">Welcome Back</h1>
                <p style="color: var(--text-secondary)">Sign in to access the control center</p>
            </div>

            <div
                style="display:flex; gap:1rem; margin-bottom:1.5rem; justify-content:center; border-bottom:1px solid var(--border-color);">
                <button class="tab-btn active" id="tabStaff" onclick="switchTab('staff')">Staff Login</button>
                <button class="tab-btn" id="tabUser" onclick="switchTab('user')">User Login</button>
            </div>

            <form id="loginForm">
                <div class="form-group">
                    <label class="form-label">Email or Phone</label>
                    <input type="text" id="identifier" class="form-input" placeholder="admin@resq.com" required>
                </div>

                <div class="form-group">
                    <label class="form-label">Password</label>
                    <input type="password" id="password" class="form-input" placeholder="••••••••" required>
                </div>

                <button type="submit" class="btn btn-primary" style="margin-top: 1rem;">Sign In</button>
            </form>

            <form id="otpForm" style="display:none;">
                <div class="form-group">
                    <label class="form-label">Phone or Email</label>
                    <input type="text" id="userIdentifier" class="form-input" placeholder="Your Phone or Email">
                </div>

                <div id="otpFields" style="display:none;">
                    <div class="form-group">
                        <label class="form-label">Enter OTP</label>
                        <input type="text" id="otpInput" class="form-input" placeholder="1234">
                    </div>
                </div>

                <button type="button" id="sendBtn" class="btn btn-primary" onclick="requestOtp()">Send OTP</button>
                <button type="button" id="verifyBtn" class="btn btn-success" onclick="doVerifyOtp()"
                    style="display:none; margin-top:1rem; width:100%;">Verify & Login</button>
            </form>

            <div id="errorMsg"
                style="color: var(--emergency-red); text-align: center; margin-top: 1rem; font-size: 0.875rem;"></div>
        </div>
    </div>

    <script src="js/main.js"></script>
    <script>
        function switchTab(mode) {
            document.getElementById('errorMsg').innerText = '';
            if (mode === 'staff') {
                document.getElementById('loginForm').style.display = 'block';
                document.getElementById('otpForm').style.display = 'none';
                document.getElementById('tabStaff').classList.add('active');
                document.getElementById('tabUser').classList.remove('active');
            } else {
                document.getElementById('loginForm').style.display = 'none';
                document.getElementById('otpForm').style.display = 'block';
                document.getElementById('tabStaff').classList.remove('active');
                document.getElementById('tabUser').classList.add('active');
            }
        }

        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const identifier = document.getElementById('identifier').value;
            const password = document.getElementById('password').value;
            performLogin('/auth/login', { email_or_phone: identifier, password });
        });

        async function requestOtp() {
            const ident = document.getElementById('userIdentifier').value;
            if (!ident) { alert('Please enter phone or email'); return; }

            const btn = document.getElementById('sendBtn');
            btn.innerText = 'Sending...';
            btn.disabled = true;

            const res = await apiCall('/auth/send-otp', 'POST', { identifier: ident });

            btn.innerText = 'Send OTP';
            btn.disabled = false;

            if (res && res.debug_otp) {
                // Show OTP field
                document.getElementById('otpFields').style.display = 'block';
                document.getElementById('sendBtn').style.display = 'none';
                document.getElementById('verifyBtn').style.display = 'inline-flex';

                // For demo convenience, show OTP in alert
                alert(`OTP Sent! Your code is: ${res.debug_otp}`);
                document.getElementById('otpInput').value = res.debug_otp; // Auto-fill for convenience
            } else {
                document.getElementById('errorMsg').innerText = res ? res.message : 'Error sending OTP';
            }
        }

        async function doVerifyOtp() {
            const ident = document.getElementById('userIdentifier').value;
            const otp = document.getElementById('otpInput').value;
            performLogin('/auth/verify-otp', { identifier: ident, otp: otp });
        }

        async function performLogin(endpoint, data) {
            const res = await apiCall(endpoint, 'POST', data);
            if (res && res.token) {
                localStorage.setItem('token', res.token);
                localStorage.setItem('user', JSON.stringify(res.user));
                if (res.user.role === 'hospital_admin') {
                    window.location.href = 'hospital_dashboard.html';
                } else if (res.user.role === 'user') {
                    window.location.href = 'user_app.html';
                } else {
                    window.location.href = 'dashboard.html';
                }
            } else {
                const msg = res ? (res.message || res.error || 'Login failed') : 'Login failed';
                document.getElementById('errorMsg').innerText = typeof msg === 'string' ? msg : 'An error occurred';
            }
        }
    </script>
</body>

</html>