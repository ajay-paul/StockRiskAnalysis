import React, { useState, useEffect } from 'react';

function RiskDashboard({ symbol }) {
    const [riskMetrics, setRiskMetrics] = useState({});

    useEffect(() => {
        fetch(`/api/risk/${symbol}/`)
            .then(response => response.json())
            .then(data => setRiskMetrics(data));
    }, [symbol]);

    return (
        <div className="RiskDashboard">
            <h2>Risk Metrics for {symbol}</h2>
            <p>Predictions: {riskMetrics.map(pred => (
                <div key={pred.id}>{pred.predicted_price}</div>
            ))}</p>
        </div>
    );
}

export default RiskDashboard;
