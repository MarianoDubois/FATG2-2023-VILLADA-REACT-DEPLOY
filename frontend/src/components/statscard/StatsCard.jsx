import React from 'react';
import Card from 'react-bootstrap/Card';

function StatsCard() {
  return (
    <Card style={{ width: '18rem', border: '1px solid #ccc' }}>
      <div style={{ textAlign: 'center', padding: '20px' }}>
        <div style={{ fontSize: '24px', fontWeight: 'bold' }}>Big Text Here</div>
        <div>Card Title</div>
      </div>
    </Card>
  );
}

export default StatsCard;
