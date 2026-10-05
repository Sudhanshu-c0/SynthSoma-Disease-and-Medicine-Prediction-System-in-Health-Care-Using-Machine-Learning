// Auth Form Client Interactions
document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.querySelector('.auth-form');
    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            const pass = document.getElementById('password');
            const confirm = document.getElementById('confirm_password');
            if (pass && confirm && pass.value !== confirm.value) {
                e.preventDefault();
                alert('Passwords do not match. Please re-enter.');
            }
        });
    }
});
