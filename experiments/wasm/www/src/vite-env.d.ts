/// <reference types="vite/client" />

declare module 'base60lab-wasm' {
  export default function init(): Promise<void>;
  export function rational_to_base60(numerator: number, denominator: number, maxDigits: number): unknown;
  export function digit_to_wedge(digit: number): string;
  export function base60_to_wedge(integerPart: Uint8Array, fractionalPart: Uint8Array): string;
  export function reciprocal_pair_add(aNum: number, aDen: number, bNum: number, bDen: number): unknown;
  export function reciprocal_pair_mul(aNum: number, aDen: number, bNum: number, bDen: number): unknown;
  export function generate_reciprocal_table(limit: number): unknown;
  export function generate_plimpton_triples(): unknown;
  export function ybc7290_sqrt2(): unknown;
  export function construct_17gon(): unknown;
  export function generate_clay_tablet_svg(width: number, height: number, content: string): string;
  export function fraction_addition_visual(aNum: number, aDen: number, bNum: number, bDen: number): unknown;
  export function get_api_info(): unknown;
}