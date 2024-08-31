import React, { useState, useEffect } from 'react';

function App() {
    const [predictedPrice, setPredictedPrice] = useState(null);

    useEffect(() => {
        fetch('/api/predict/reliance/')
            .then(response => response.json())
            .then(data => setPredictedPrice(data.predicted_price));
    }, []);

    return (
        <div className="App">
            <h1>Stock Prediction Dashboard</h1>
            {predictedPrice ? (
                <div>
                    <h2>Predicted Price for Reliance:</h2>
                    <p>{predictedPrice}</p>
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
}

export default App;
