/**
 * background-animation.js
 * 
 * Creates a twinkling and gently moving starfield effect on a canvas element.
 * This is designed to be used as a background for the entire site.
 */
document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('starfield');
    if (!canvas) {
        console.error('Starfield canvas not found!');
        return;
    }

    const ctx = canvas.getContext('2d');

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    const numStars = 200;
    const stars = [];

    for (let i = 0; i < numStars; i++) {
        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 1.5 + 0.5, // Star size
            alpha: Math.random(), // Initial opacity
            deltaAlpha: Math.random() * 0.02 - 0.01 // How fast it twinkles
        });
    }

    function drawStars() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Determine star color based on theme
        const isDarkMode = document.documentElement.getAttribute('data-theme') === 'dark';
        const starColor = isDarkMode ? 'rgba(255, 255, 255, ' : 'rgba(0, 0, 0, ';

        stars.forEach(star => {
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
            ctx.fillStyle = starColor + star.alpha + ')';
            ctx.fill();
        });
    }

    function updateStars() {
        stars.forEach(star => {
            // Twinkle effect
            star.alpha += star.deltaAlpha;
            if (star.alpha <= 0 || star.alpha >= 1) {
                star.deltaAlpha *= -1;
            }

            // Slow movement
            star.x -= 0.1;
            if (star.x < 0) {
                star.x = canvas.width;
            }
        });
    }

    function animate() {
        drawStars();
        updateStars();
        requestAnimationFrame(animate);
    }

    animate();
});