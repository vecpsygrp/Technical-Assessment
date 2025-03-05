// Type definitions for the calculator

export type OperatorType = '+' | '-' | '*' | '/' | '=';

export interface CalculationState {
  currentValue: string;
  previousValue: string;
  operator: OperatorType | null;
  waitingForOperand: boolean;
}
