document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                password
            })
        });
        const data = await response.json();
        if (response.ok) {
            // Login successful, redirect to dashboard
            window.location.href = "../templates/dashboard.html";
        } else {
            // Login failed, display error message
            document.getElementById('loginMessage').textContent = data.detail;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('loginMessage').textContent = 'An error occurred';
    }
});


document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                password
            })
        });
        const data = await response.json();
        document.getElementById('registerMessage').textContent = data.message;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('registerMessage').textContent = 'An error occurred';
    }
});

// scripts.js
function toggleForm(formName) {
    if (formName === 'login') {
        document.getElementById('loginContainer').style.display = 'block';
        document.getElementById('registerContainer').style.display = 'none';
    } else if (formName === 'register') {
        document.getElementById('loginContainer').style.display = 'none';
        document.getElementById('registerContainer').style.display = 'block';
    }
}


// scripts.js
function toggleForm(formName) {
    if (formName === 'login') {
        document.getElementById('loginContainer').style.display = 'block';
        document.getElementById('registerContainer').style.display = 'none';
    } else if (formName === 'register') {
        document.getElementById('loginContainer').style.display = 'none';
        document.getElementById('registerContainer').style.display = 'block';
    }
}
