// TypeScript types for the WASM module

export interface Base60Digits {
  integer_part: number[];
  fractional_part: number[];
  is_repeating: boolean;
  repeating_start: number | null;
}

export interface ReciprocalEntry {
  n: number;
  reciprocal_numerator: number;
  reciprocal_denominator: number;
  base60: Base60Digits;
  wedge: string;
  terminates: boolean;
}

export interface FractionResult {
  numerator: number;
  denominator: number;
  base60: Base60Digits;
  wedge: string;
  steps: string[];
}

export interface PlimptonTriple {
  row: number;
  p: number;
  q: number;
  a: number;
  b: number;
  c: number;
  ratio_a_c: string;
  wedge_a: string;
  wedge_b: string;
  wedge_c: string;
}

export interface Sqrt2Result {
  babylonian_approximation: string;
  babylonian_wedge: string;
  exact_base60: string;
  exact_wedge: string;
  decimal_approximation: number;
  decimal_exact: number;
  error: number;
  clay_tablet_notation: string;
}

export interface Vertex {
  index: number;
  angle_rad: number;
  x: number;
  y: number;
  x_wedge: string;
  y_wedge: string;
}

export interface Gon17Result {
  vertices: Vertex[];
  construction_steps: string[];
  gauss_expression: string;
}

export interface VisualData {
  a_wedge: string;
  b_wedge: string;
  sum_wedge: string;
  a_base60: Base60Digits;
  b_base60: Base60Digits;
  sum_base60: Base60Digits;
  common_denominator: number;
  steps: string[];
  a_parts: number[];
  b_parts: number[];
  sum_parts: number[];
}

export interface ApiInfo {
  version: string;
  functions: string[];
}