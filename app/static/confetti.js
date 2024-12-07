function startConfetti() {
    const confettiContainer = document.getElementById('confetti-container');
    confettiContainer.style.display = 'block';
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff', '#ffffff', '#ff8800'];
    const numConfetti = 100;
    const centerX = window.innerWidth / 2;
    const centerY = window.innerHeight / 2;

    for (let i = 0; i < numConfetti; i++) {
        const piece = document.createElement('div');
        piece.classList.add('confetti-piece');
        const color = colors[Math.floor(Math.random()*colors.length)];
        piece.style.backgroundColor = color;

        // Случайные направления и дальности разлёта
        const angle = Math.random() * 2 * Math.PI;
        const distance = (Math.random() * 400) + 200; // отлетят на 200-600px
        const x = Math.cos(angle) * distance;
        const y = Math.sin(angle) * distance;

        // Случайный угол вращения
        const rotate = `${Math.random() * 720 - 360}deg`;

        piece.style.setProperty('--x', x + 'px');
        piece.style.setProperty('--y', y + 'px');
        piece.style.setProperty('--r', rotate);

        // Стартуем из центра экрана
        piece.style.left = centerX + 'px';
        piece.style.top = centerY + 'px';

        piece.style.animationDuration = (Math.random() * 1 + 1) + 's'; // 1-2 сек

        confettiContainer.appendChild(piece);
    }
}
