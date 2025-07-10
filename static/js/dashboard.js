const socket = io();

socket.on('connect', function () {
    document.getElementById('status').className = 'status connected';
    document.getElementById('status').textContent = 'Connected - Real-time updates active';
});

socket.on('disconnect', function () {
    document.getElementById('status').className = 'status disconnected';
    document.getElementById('status').textContent = 'Disconnected - Reconnecting...';
});

socket.on('new_measurement', function (data) {
    updateDisplay(data);
});

function formatTimestamp(timestamp) {
    const date = new Date(timestamp * 1000);
    return date.toLocaleString();
}

function updateDisplay(measurement) {
    if (!measurement || !measurement.data) {
        return;
    }

    const content = `
        <div class="timestamp">
            <strong>Last Update:</strong> ${formatTimestamp(measurement.timestamp)}
        </div>
        
        <div class="section">
            <h2>Water Level</h2>
            <div class="value">
                <strong>Level:</strong> ${measurement.data.water_level} mm
            </div>
        </div>
        
        <div class="section">
            <h2>Inside Measurements</h2>
            <div class="measurement">
                <div class="value">
                    <strong>Up - Temperature:</strong> ${measurement.data.inside.up.temperature}°C
                </div>
                <div class="value">
                    <strong>Up - Humidity:</strong> ${measurement.data.inside.up.humidity}%
                </div>
                <div class="value">
                    <strong>Down - Temperature:</strong> ${measurement.data.inside.down.temperature}°C
                </div>
                <div class="value">
                    <strong>Down - Humidity:</strong> ${measurement.data.inside.down.humidity}%
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>Outside Measurements</h2>
            <div class="measurement">
                <div class="value">
                    <strong>Up - Temperature:</strong> ${measurement.data.outside.up.temperature}°C
                </div>
                <div class="value">
                    <strong>Up - Humidity:</strong> ${measurement.data.outside.up.humidity}%
                </div>
                <div class="value">
                    <strong>Up - Lux:</strong> ${measurement.data.outside.up.lux} lux
                </div>
                <div class="value">
                    <strong>Down - Temperature:</strong> ${measurement.data.outside.down.temperature}°C
                </div>
                <div class="value">
                    <strong>Down - Humidity:</strong> ${measurement.data.outside.down.humidity}%
                </div>
                <div class="value">
                    <strong>Down - Lux:</strong> ${measurement.data.outside.down.lux} lux
                </div>
            </div>
        </div>
    `;

    document.getElementById('content').innerHTML = content;
}

// Request latest measurement on page load
socket.emit('request_latest');