// static/js/auth.js (Corrected Code)

document.addEventListener('DOMContentLoaded', () => {

    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = Object.fromEntries(new FormData(registerForm).entries());
            
            try {
                const res = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                const result = await res.json();
                
                if (res.ok) {
                    alert('Registration successful! Please log in.');
                    window.location.href = '/login'; // Redirect to login
                } else {
                    alert(`Registration failed: ${result.error}`);
                }
            } catch (err) {
                console.error(err);
                alert('Network error during registration.');
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = Object.fromEntries(new FormData(loginForm).entries());
            
            try {
                const res = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                
                const result = await res.json();
                
                if (res.ok) {
                    alert('Login successful!');
                    // This is the line that performs the redirect
                    window.location.href = result.dashboard_url;
                } else {
                    alert(`Login failed: ${result.error}`);
                }
            } catch (err) {
                console.error(err);
                alert('Network error during login.');
            }
        });
    }
});