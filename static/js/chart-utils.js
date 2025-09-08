// Chart Utilities Module

// Initialize Weather Charts
function initWeatherCharts() {
    // Wind Line Chart
    const windLineCtx = document.getElementById('windLineChart').getContext('2d');
    new Chart(windLineCtx, {
        type: 'line',
        data: {
            labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
            datasets: [{
                data: [5.2, 6.8, 7.9, 8.1, 7.3, 6.5],
                borderColor: 'rgba(255,255,255,0.8)',
                backgroundColor: 'transparent',
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { display: false },
                y: { display: false }
            }
        }
    });

    // Wind Bar Chart
    const windBarCtx = document.getElementById('windBarChart').getContext('2d');
    new Chart(windBarCtx, {
        type: 'bar',
        data: {
            labels: ['1', '2', '3', '4', '5', '6', '7', '8'],
            datasets: [{
                data: [3, 5, 4, 7, 6, 8, 5, 4],
                backgroundColor: 'rgba(255,255,255,0.3)',
                borderColor: 'rgba(255,255,255,0.5)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { display: false },
                y: { display: false }
            }
        }
    });

    // Sun Arc Chart
    const sunArcCtx = document.getElementById('sunArcChart').getContext('2d');
    new Chart(sunArcCtx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [75, 25],
                backgroundColor: ['rgba(255,255,255,0.1)', 'transparent'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '80%',
            plugins: { legend: { display: false } }
        }
    });
}

// Initialize River Height Chart
function initRiverHeightChart() {
    const ctx = document.getElementById('riverHeightChart').getContext('2d');
    
    const riverHeightChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'River Height (m)',
                data: [1.2, 2.1, 3.5, 2.8, 1.9, 2.3, 1.7],
                borderColor: 'rgba(255, 255, 255, 0.7)',
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(255, 255, 255, 0.9)',
                pointBorderColor: 'rgba(255, 255, 255, 0.5)',
                pointBorderWidth: 1,
                pointRadius: 3,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: 'rgba(255, 255, 255, 1)',
                pointHoverBorderColor: 'rgba(255, 255, 255, 0.7)',
                pointHoverBorderWidth: 2,
                tension: 0.4,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: {
                    top: 20,
                    bottom: 5,
                    left: 15,
                    right: 15
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: true,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: 'white',
                    bodyColor: 'white',
                    borderColor: 'rgba(255, 255, 255, 0.2)',
                    borderWidth: 1,
                    borderRadius: 6,
                    padding: 8,
                    titleFont: {
                        family: 'Segoe UI, -apple-system, BlinkMacSystemFont, Inter, Roboto, sans-serif',
                        size: 10,
                        weight: 500
                    },
                    bodyFont: {
                        family: 'Segoe UI, -apple-system, BlinkMacSystemFont, Inter, Roboto, sans-serif',
                        size: 9,
                        weight: 400
                    },
                    displayColors: false,
                    position: 'nearest',
                    xAlign: 'center',
                    yAlign: 'bottom',
                    caretSize: 4,
                    callbacks: {
                        title: function(context) {
                            const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
                            return days[context[0].dataIndex];
                        },
                        label: function(context) {
                            return context.parsed.y + 'm';
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: false
                },
                y: {
                    display: false
                }
            },
            elements: {
                point: {
                    hoverBackgroundColor: 'rgba(255, 255, 255, 1)'
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            },
            animation: {
                duration: 2000,
                easing: 'easeInOutQuart',
                onComplete: function() {
                    // Add custom labels after chart is drawn
                    addCustomLabels(riverHeightChart);
                }
            },
            transitions: {
                show: {
                    animations: {
                        x: {
                            from: 0
                        },
                        y: {
                            from: 0
                        }
                    }
                },
                hide: {
                    animations: {
                        x: {
                            to: 0
                        },
                        y: {
                            to: 0
                        }
                    }
                }
            }
        }
    });
}

// Add custom labels to charts
function addCustomLabels(chart) {
    const ctx = chart.ctx;
    const data = chart.data.datasets[0].data;
    const meta = chart.getDatasetMeta(0);
    const chartArea = chart.chartArea;
    
    ctx.save();
    ctx.font = '10px Segoe UI, -apple-system, BlinkMacSystemFont, Inter, Roboto, sans-serif';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.textBaseline = 'top';
    
    meta.data.forEach((point, index) => {
        const x = point.x;
        let y = point.y + 25; // Position below the point with more spacing
        
        // Ensure labels don't go below the chart area
        if (y > chartArea.bottom - 30) {
            y = chartArea.bottom - 30;
        }
        
        // Adjust text alignment for edge points
        if (index === 0) {
            ctx.textAlign = 'left';
        } else if (index === data.length - 1) {
            ctx.textAlign = 'right';
        } else {
            ctx.textAlign = 'center';
        }
        
        ctx.fillText(data[index] + 'm', x, y);
    });
    
    ctx.restore();
}
