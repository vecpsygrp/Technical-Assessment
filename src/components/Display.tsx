import React from 'react';

interface DisplayProps {
  value: string;
}

const Display: React.FC<DisplayProps> = ({ value }) => {
  return (
    <div className="calculator-display">
      <div className="display-value">{value}</div>
    </div>
  );
};

export default Display;
