// Add your TypeScript interfaces and types here

export type OperatorType = '+' | '-' | '*' | '/' | '=';

export interface CalculationState {
  currentValue: string;
  previousValue: string;
  operator: OperatorType | null;
  waitingForOperand: boolean;
}

// Add more types as needed by the application
