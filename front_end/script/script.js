// script.js

document.addEventListener('DOMContentLoaded', () => {
    const chipSelector = document.querySelector('.chip-selector');
    const bettingCells = document.querySelectorAll('#betting-grid .cell');
    const totalBetDisplay = document.getElementById('total-bet-display');
    
    let selectedChipValue = 1; // Default chip value
    let totalBet = 50.00;

    // --- 1. Chip Selection ---
    chipSelector.addEventListener('click', (event) => {
        if (event.target.classList.contains('chip')) {
            // Remove 'active' class from all chips
            document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
            
            // Set new active chip and value
            event.target.classList.add('active');
            selectedChipValue = parseFloat(event.target.getAttribute('data-value'));
            console.log(`Selected chip value: ${selectedChipValue}`);
        }
    });

    // Initialize the default selected chip
    document.querySelector('.chip[data-value="1"]').classList.add('active');


    // --- 2. Placing Bets ---
    bettingCells.forEach(cell => {
        cell.addEventListener('click', () => {
            const betType = cell.getAttribute('data-bet');
            
            // For a basic UI, we just simulate the placement of a chip
            const chipMarker = document.createElement('div');
            chipMarker.classList.add('bet-chip-marker');
            chipMarker.textContent = selectedChipValue;
            chipMarker.style.backgroundColor = getChipColor(selectedChipValue); // Dynamic color based on value

            // Simple placement at the center of the cell
            cell.appendChild(chipMarker);

            // Update Total Bet
            totalBet += selectedChipValue;
            totalBetDisplay.textContent = totalBet.toFixed(2);

            console.log(`Bet placed on: ${betType} with value ${selectedChipValue}`);
        });
    });

    // Helper function to assign a color to the visual bet marker
    function getChipColor(value) {
        if (value === 0.5) return '#880e4f';
        if (value === 1) return '#38761d';
        if (value === 5) return '#0c3498';
        if (value === 10) return '#d58c14'; // New color
        if (value === 25) return '#990000'; // New color
        if (value === 100) return '#3d3d3d'; // New color
        return '#fff';
    }

    // --- 3. Wheel Spin Simulation (Optional) ---
    const playButton = document.querySelector('.play-btn');
    const wheelInnerRing = document.querySelector('.wheel-inner-ring');

    playButton.addEventListener('click', () => {
        // Stop any current animation and restart it for a new spin effect
        wheelInnerRing.style.animation = 'none';
        void wheelInnerRing.offsetWidth; // Trigger reflow
        
        // Simulate a new spin with a random duration and a more complex easing function
        const spinDuration = 3 + Math.random() * 2; // 3 to 5 seconds
        // Using ease-out simulates the wheel slowing down
        wheelInnerRing.style.animation = `spin-wheel ${spinDuration}s cubic-bezier(0.1, 0.7, 1.0, 0.1) forwards`;
        
        // In a real game, you would calculate the final stop position here.
        setTimeout(() => {
            console.log('Spin complete. Ready for next bet.');
            // Revert to a slow idle spin or stop completely
            wheelInnerRing.style.animation = 'spin-wheel 5s linear infinite';
        }, spinDuration * 1000);
    });

});