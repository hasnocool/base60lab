// WASM module loader and wrapper

import type { 
  Base60Digits, 
  ReciprocalEntry, 
  FractionResult,
  PlimptonTriple,
  Sqrt2Result,
  Gon17Result,
  VisualData,
  ApiInfo
} from './types';

interface WasmModule {
  rational_to_base60: (numerator: number, denominator: number, maxDigits: number) => Base60Digits;
  digit_to_wedge: (digit: number) => string;
  base60_to_wedge: (integerPart: Uint8Array, fractionalPart: Uint8Array) => string;
  reciprocal_pair_add: (aNum: number, aDen: number, bNum: number, bDen: number) => FractionResult;
  reciprocal_pair_mul: (aNum: number, aDen: number, bNum: number, bDen: number) => FractionResult;
  generate_reciprocal_table: (limit: number) => ReciprocalEntry[];
  generate_plimpton_triples: () => PlimptonTriple[];
  ybc7290_sqrt2: () => Sqrt2Result;
  construct_17gon: () => Gon17Result;
  generate_clay_tablet_svg: (width: number, height: number, content: string) => string;
  fraction_addition_visual: (aNum: number, aDen: number, bNum: number, bDen: number) => VisualData;
  get_api_info: () => ApiInfo;
  default: () => Promise<void>;
}

let wasmModule: WasmModule | null = null;

export async function loadWasm(): Promise<WasmModule> {
  if (wasmModule) return wasmModule;
  
  try {
    // Import the WASM module
    const wasm = await import('base60lab-wasm');
    await wasm.default();
    wasmModule = wasm as unknown as WasmModule;
    console.log('WASM module loaded:', wasmModule.get_api_info());
    return wasmModule;
  } catch (error) {
    console.error('Failed to load WASM module:', error);
    throw error;
  }
}

export function getWasm(): WasmModule {
  if (!wasmModule) {
    throw new Error('WASM module not loaded. Call loadWasm() first.');
  }
  return wasmModule;
}

// Wrapper functions with proper typing
export async function rationalToBase60(numerator: number, denominator: number, maxDigits = 20): Promise<Base60Digits> {
  const wasm = await loadWasm();
  return wasm.rational_to_base60(numerator, denominator, maxDigits);
}

export async function digitToWedge(digit: number): Promise<string> {
  const wasm = await loadWasm();
  return wasm.digit_to_wedge(digit);
}

export async function base60ToWedge(integerPart: number[], fractionalPart: number[]): Promise<string> {
  const wasm = await loadWasm();
  return wasm.base60_to_wedge(new Uint8Array(integerPart), new Uint8Array(fractionalPart));
}

export async function reciprocalPairAdd(aNum: number, aDen: number, bNum: number, bDen: number): Promise<FractionResult> {
  const wasm = await loadWasm();
  return wasm.reciprocal_pair_add(aNum, aDen, bNum, bDen);
}

export async function reciprocalPairMul(aNum: number, aDen: number, bNum: number, bDen: number): Promise<FractionResult> {
  const wasm = await loadWasm();
  return wasm.reciprocal_pair_mul(aNum, aDen, bNum, bDen);
}

export async function generateReciprocalTable(limit: number): Promise<ReciprocalEntry[]> {
  const wasm = await loadWasm();
  return wasm.generate_reciprocal_table(limit);
}

export async function generatePlimptonTriples(): Promise<PlimptonTriple[]> {
  const wasm = await loadWasm();
  return wasm.generate_plimpton_triples();
}

export async function ybc7290Sqrt2(): Promise<Sqrt2Result> {
  const wasm = await loadWasm();
  return wasm.ybc7290_sqrt2();
}

export async function construct17gon(): Promise<Gon17Result> {
  const wasm = await loadWasm();
  return wasm.construct_17gon();
}

export async function generateClayTabletSvg(width: number, height: number, content: string): Promise<string> {
  const wasm = await loadWasm();
  return wasm.generate_clay_tablet_svg(width, height, content);
}

export async function fractionAdditionVisual(aNum: number, aDen: number, bNum: number, bDen: number): Promise<VisualData> {
  const wasm = await loadWasm();
  return wasm.fraction_addition_visual(aNum, aDen, bNum, bDen);
}

export async function getApiInfo(): Promise<ApiInfo> {
  const wasm = await loadWasm();
  return wasm.get_api_info();
}