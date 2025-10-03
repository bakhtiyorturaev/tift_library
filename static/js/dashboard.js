document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts
    if (document.getElementById('loansChart')) {
        const ctx = document.getElementById('loansChart').getContext('2d');
        const labels = JSON.parse(document.getElementById('loansChart').dataset.labels);
        const data = JSON.parse(document.getElementById('loansChart').dataset.values);

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Ijaralar soni',
                    data: data,
                    backgroundColor: 'rgba(78, 115, 223, 0.8)',
                    borderColor: 'rgba(78, 115, 223, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }
});