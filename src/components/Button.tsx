import React from 'react';

interface ButtonProps {
  value: string;
  onClick: (value: string) => void;
  className?: string;
}

const Button: React.FC<ButtonProps> = ({ value, onClick, className }) => {
  const handleClick = () => {
    onClick(value);
  };

  return (
    <button 
      className={`calculator-button ${className || ''}`} 
      onClick={handleClick}
    >
      {value}
    </button>
  );
};

export default Button;
