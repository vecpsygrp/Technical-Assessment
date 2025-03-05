import React, { useState } from 'react';
import Display from './Display';
import Button from './Button';
import '../styles/Calculator.css';

// TODO: Candidate should implement this component to create a working calculator

const Calculator: React.FC = () => {
  const [display, setDisplay] = useState('0');
  // TODO: Add necessary state variables to track calculations

  // TODO: Implement button click handlers for numbers, operators, and special functions
  
  const handleButtonClick = (value: string) => {
    // This is a stub function that the candidate should implement
    console.log(`Button clicked: ${value}`);
    
    // Placeholder implementation - simply updates display with clicked value
    if (display === '0') {
      setDisplay(value);
    } else {
      setDisplay(display + value);
    }
  };

  return (
    <div className="calculator">
      <Display value={display} />
      <div className="calculator-keypad">
        {/* TODO: Implement calculator buttons */}
        <div className="calculator-row">
          <Button value="7" onClick={handleButtonClick} />
          <Button value="8" onClick={handleButtonClick} />
          <Button value="9" onClick={handleButtonClick} />
          <Button value="/" onClick={handleButtonClick} className="operator" />
        </div>
        <div className="calculator-row">
          <Button value="4" onClick={handleButtonClick} />
          <Button value="5" onClick={handleButtonClick} />
          <Button value="6" onClick={handleButtonClick} />
          <Button value="*" onClick={handleButtonClick} className="operator" />
        </div>
        <div className="calculator-row">
          <Button value="1" onClick={handleButtonClick} />
          <Button value="2" onClick={handleButtonClick} />
          <Button value="3" onClick={handleButtonClick} />
          <Button value="-" onClick={handleButtonClick} className="operator" />
        </div>
        <div className="calculator-row">
          <Button value="0" onClick={handleButtonClick} />
          <Button value="." onClick={handleButtonClick} />
          <Button value="=" onClick={handleButtonClick} className="equals" />
          <Button value="+" onClick={handleButtonClick} className="operator" />
        </div>
        <div className="calculator-row">
          <Button value="C" onClick={handleButtonClick} className="clear" />
        </div>
      </div>
    </div>
  );
};

export default Calculator;
