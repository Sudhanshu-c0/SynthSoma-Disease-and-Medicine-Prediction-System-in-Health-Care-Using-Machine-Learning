// SynthSoma Main JavaScript Client Script

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Toggle
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('open');
            const icon = navToggle.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-bars');
                icon.classList.toggle('fa-xmark');
            }
        });
    }

    // 2. Auto-dismiss alerts after 6 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 400);
        }, 6000);
    });
});

function openDisclaimerModal(e) {
    if (e) e.preventDefault();
    alert(
        "MANDATORY CLINICAL DISCLAIMER:\n\n" +
        "SynthSoma is an academic and reference intelligence prototype. " +
        "The disease predictions, reference medicine records, lifestyle precautions, " +
        "and risk factor assessments are generated for educational and informational purposes only.\n\n" +
        "This platform does NOT replace certified clinical examination, professional diagnosis, " +
        "or physician prescription. In any health emergency, contact local emergency healthcare providers immediately."
    );
}
