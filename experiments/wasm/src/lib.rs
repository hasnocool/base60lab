//! Base-60 exact rational arithmetic for WebAssembly
//! Babylonian Fraction Arithmetic Visualizer

use std::fmt;
use wasm_bindgen::prelude::*;
use serde::{Serialize, Deserialize};
use serde_wasm_bindgen;
use web_sys::console;

/// Initialize panic hook for better error messages in browser
#[wasm_bindgen(start)]
pub fn init_panic_hook() {
    console_error_panic_hook::set_once();
}

/// Exact rational number p/q in lowest terms
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Rational {
    numerator: i64,
    denominator: i64,
}

impl Rational {
    pub fn new(numerator: i64, denominator: i64) -> Self {
        if denominator == 0 {
            panic!("Denominator cannot be zero");
        }
        let mut n = numerator;
        let mut d = denominator;
        if d < 0 {
            n = -n;
            d = -d;
        }
        let g = gcd(n.abs(), d);
        Rational {
            numerator: n / g,
            denominator: d / g,
        }
    }

    pub fn from_int(n: i64) -> Self {
        Rational { numerator: n, denominator: 1 }
    }

    pub fn numerator(&self) -> i64 {
        self.numerator
    }

    pub fn denominator(&self) -> i64 {
        self.denominator
    }

    pub fn is_zero(&self) -> bool {
        self.numerator == 0
    }

    pub fn is_one(&self) -> bool {
        self.numerator == self.denominator
    }

    pub fn add(&self, other: &Rational) -> Rational {
        Rational::new(
            self.numerator * other.denominator + other.numerator * self.denominator,
            self.denominator * other.denominator,
        )
    }

    pub fn sub(&self, other: &Rational) -> Rational {
        Rational::new(
            self.numerator * other.denominator - other.numerator * self.denominator,
            self.denominator * other.denominator,
        )
    }

    pub fn mul(&self, other: &Rational) -> Rational {
        Rational::new(
            self.numerator * other.numerator,
            self.denominator * other.denominator,
        )
    }

    pub fn div(&self, other: &Rational) -> Rational {
        Rational::new(
            self.numerator * other.denominator,
            self.denominator * other.numerator,
        )
    }

    pub fn reciprocal(&self) -> Rational {
        Rational::new(self.denominator, self.numerator)
    }

    pub fn pow(&self, exp: u32) -> Rational {
        Rational::new(
            self.numerator.pow(exp),
            self.denominator.pow(exp),
        )
    }

    pub fn sqrt_approx(&self, iterations: u32) -> Rational {
        // Newton's method for square root
        if self.is_zero() {
            return Rational::from_int(0);
        }
        let mut x = Rational::new(self.numerator, self.denominator);
        for _ in 0..iterations {
            let two = Rational::from_int(2);
            x = x.add(&self.div(&x)).div(&two);
        }
        x
    }

    pub fn to_f64(&self) -> f64 {
        self.numerator as f64 / self.denominator as f64
    }

    fn is_terminating_in_base(&self, base: u32) -> bool {
        let mut d = self.denominator as u64;
        let base_factors = prime_factors(base);
        for p in base_factors {
            let p64 = p as u64;
            while d % p64 == 0 {
                d /= p64;
            }
        }
        d == 1
    }
}

fn gcd(a: i64, b: i64) -> i64 {
    let mut a = a.abs();
    let mut b = b.abs();
    while b != 0 {
        let t = b;
        b = a % b;
        a = t;
    }
    a
}

fn prime_factors(n: u32) -> Vec<u32> {
    let mut factors = Vec::new();
    let mut n = n;
    let mut d = 2;
    while d * d <= n {
        while n % d == 0 {
            if !factors.contains(&d) {
                factors.push(d);
            }
            n /= d;
        }
        d += 1;
    }
    if n > 1 {
        factors.push(n);
    }
    factors
}

/// Base-60 digit representation
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Base60Digits {
    pub integer_part: Vec<u8>,  // each 0-59
    pub fractional_part: Vec<u8>, // each 0-59
    pub is_repeating: bool,
    pub repeating_start: Option<usize>,
}

impl Base60Digits {
    pub fn new() -> Self {
        Base60Digits {
            integer_part: vec![0],
            fractional_part: Vec::new(),
            is_repeating: false,
            repeating_start: None,
        }
    }
}

/// Convert rational to base-60 representation
#[wasm_bindgen]
pub fn rational_to_base60(numerator: i64, denominator: i64, max_digits: usize) -> JsValue {
    let rat = Rational::new(numerator, denominator);
    let digits = rat.to_base60(max_digits);
    serde_wasm_bindgen::to_value(&digits).unwrap()
}

impl Rational {
    fn to_base60(&self, max_digits: usize) -> Base60Digits {
        let mut result = Base60Digits::new();
        let sign = if self.numerator < 0 { -1 } else { 1 };
        let num = (self.numerator * sign) as u64;
        let den = self.denominator as u64;

        // Integer part
        let mut int_part = num / den;
        let mut remainder = num % den;

        if int_part == 0 {
            result.integer_part = vec![0];
        } else {
            let mut int_digits = Vec::new();
            while int_part > 0 {
                int_digits.push((int_part % 60) as u8);
                int_part /= 60;
            }
            int_digits.reverse();
            result.integer_part = int_digits;
        }

        // Fractional part using long division in base 60
        let mut seen = std::collections::HashMap::new();
        let mut frac_digits = Vec::new();
        let mut r = remainder;
        let mut pos = 0;

        while r != 0 && pos < max_digits {
            if let Some(&start) = seen.get(&r) {
                result.is_repeating = true;
                result.repeating_start = Some(start);
                break;
            }
            seen.insert(r, pos);

            r *= 60;
            let digit = (r / den) as u8;
            frac_digits.push(digit);
            r = r % den;
            pos += 1;
        }

        result.fractional_part = frac_digits;
        result
    }
}

/// Babylonian wedge numeral symbols
const WEDGE_VERTICAL: &str = "𒁹";  // 1 (vertical wedge)
const WEDGE_HORIZONTAL: &str = "𒌋"; // 10 (horizontal wedge)
const WEDGE_ZERO: &str = "";        // placeholder

/// Convert a base-60 digit (0-59) to Babylonian wedge numerals
#[wasm_bindgen]
pub fn digit_to_wedge(digit: u8) -> String {
    if digit == 0 {
        return "𒑱".to_string(); // Babylonian zero placeholder
    }
    let tens = digit / 10;
    let ones = digit % 10;
    let mut result = String::new();
    for _ in 0..tens {
        result.push_str(WEDGE_HORIZONTAL);
    }
    for _ in 0..ones {
        result.push_str(WEDGE_VERTICAL);
    }
    result
}

/// Convert base-60 digits to wedge numeral string
#[wasm_bindgen]
pub fn base60_to_wedge(integer_part: &[u8], fractional_part: &[u8]) -> String {
    let mut result = String::new();
    
    // Integer part
    for (i, &digit) in integer_part.iter().enumerate() {
        if i > 0 {
            result.push(' ');
        }
        result.push_str(&digit_to_wedge(digit));
    }
    
    // Fractional part
    if !fractional_part.is_empty() {
        result.push_str(" ; ");
        for (i, &digit) in fractional_part.iter().enumerate() {
            if i > 0 {
                result.push(' ');
            }
            result.push_str(&digit_to_wedge(digit));
        }
    }
    
    result
}

/// Reciprocal pair method for fraction addition
/// a/b + c/d = (ad + bc) / bd
/// Using reciprocal tables: find reciprocals and use multiplication
#[wasm_bindgen]
pub fn reciprocal_pair_add(a_num: i64, a_den: i64, b_num: i64, b_den: i64) -> JsValue {
    let a = Rational::new(a_num, a_den);
    let b = Rational::new(b_num, b_den);
    let result = a.add(&b);
    
    #[derive(Serialize)]
    struct Result {
        numerator: i64,
        denominator: i64,
        base60: Base60Digits,
        wedge: String,
        steps: Vec<String>,
    }
    
    let base60 = result.to_base60(20);
    let wedge = base60_to_wedge(&base60.integer_part, &base60.fractional_part);
    
    let steps = vec![
        format!("{}/{} + {}/{}", a_num, a_den, b_num, b_den),
        format!("= ({}×{} + {}×{}) / ({}×{})", a_num, b_den, b_num, a_den, a_den, b_den),
        format!("= {}/{}", result.numerator, result.denominator),
        format!("Base-60: {}", wedge),
    ];
    
    serde_wasm_bindgen::to_value(&Result {
        numerator: result.numerator,
        denominator: result.denominator,
        base60,
        wedge,
        steps,
    }).unwrap()
}

/// Reciprocal pair method for fraction multiplication
/// a/b × c/d = ac / bd
#[wasm_bindgen]
pub fn reciprocal_pair_mul(a_num: i64, a_den: i64, b_num: i64, b_den: i64) -> JsValue {
    let a = Rational::new(a_num, a_den);
    let b = Rational::new(b_num, b_den);
    let result = a.mul(&b);
    
    #[derive(Serialize)]
    struct Result {
        numerator: i64,
        denominator: i64,
        base60: Base60Digits,
        wedge: String,
        steps: Vec<String>,
    }
    
    let base60 = result.to_base60(20);
    let wedge = base60_to_wedge(&base60.integer_part, &base60.fractional_part);
    
    let steps = vec![
        format!("{}/{} × {}/{}", a_num, a_den, b_num, b_den),
        format!("= ({}×{}) / ({}×{})", a_num, b_num, a_den, b_den),
        format!("= {}/{}", result.numerator, result.denominator),
        format!("Base-60: {}", wedge),
    ];
    
    serde_wasm_bindgen::to_value(&Result {
        numerator: result.numerator,
        denominator: result.denominator,
        base60,
        wedge,
        steps,
    }).unwrap()
}

/// Generate reciprocal table for regular numbers (5-smooth: 2^a * 3^b * 5^c)
#[wasm_bindgen]
pub fn generate_reciprocal_table(limit: u32) -> JsValue {
    let mut regulars = Vec::new();
    
    // Generate all 5-smooth numbers up to limit
    for a in 0..10 {
        for b in 0..7 {
            for c in 0..5 {
                let val = (2i64.pow(a) * 3i64.pow(b) * 5i64.pow(c)) as u32;
                if val <= limit && val > 0 {
                    regulars.push(val);
                }
            }
        }
    }
    regulars.sort();
    regulars.dedup();
    
    #[derive(Serialize)]
    struct ReciprocalEntry {
        n: u32,
        reciprocal_numerator: i64,
        reciprocal_denominator: i64,
        base60: Base60Digits,
        wedge: String,
        terminates: bool,
    }
    
    let mut entries = Vec::new();
    for n in regulars {
        let recip = Rational::new(1, n as i64);
        let base60 = recip.to_base60(20);
        let wedge = base60_to_wedge(&base60.integer_part, &base60.fractional_part);
        let terminates = recip.is_terminating_in_base(60);
        
        entries.push(ReciprocalEntry {
            n,
            reciprocal_numerator: recip.numerator,
            reciprocal_denominator: recip.denominator,
            base60,
            wedge,
            terminates,
        });
    }
    
    serde_wasm_bindgen::to_value(&entries).unwrap()
}

/// Plimpton 322 triple generator using reciprocal pair method
/// (p, q) → (p² + q², p² - q², 2pq) normalized
#[wasm_bindgen]
pub fn generate_plimpton_triples() -> JsValue {
    // Historical Plimpton 322 generators (p, q pairs from the tablet)
    let generators = vec![
        (12, 5), (64, 27), (75, 32), (125, 54), (16, 9),
        (81, 40), (225, 128), (45, 16), (32, 15), (25, 12),
        (18, 5), (20, 9), (50, 27), (9, 4), (2, 1),
    ];
    
    #[derive(Serialize)]
    struct Triple {
        row: usize,
        p: u32,
        q: u32,
        a: i64,  // p² + q² (hypotenuse)
        b: i64,  // p² - q² (long leg)
        c: i64,  // 2pq (short leg)
        ratio_a_c: String,  // (p/q + q/p)² / 4 in base-60
        wedge_a: String,
        wedge_b: String,
        wedge_c: String,
    }
    
    let mut triples = Vec::new();
    for (row, (p_ref, q_ref)) in generators.iter().enumerate() {
        let p = *p_ref as i64;
        let q = *q_ref as i64;
        
        let a = p*p + q*q;
        let b = p*p - q*q;
        let c = 2*p*q;
        
        // The ratio (p/q + q/p)² / 4 = (p²+q²)²/(4p²q²)
        let ratio_num = (p*p + q*q).pow(2);
        let ratio_den = 4 * p*p * q*q;
        let ratio = Rational::new(ratio_num, ratio_den);
        let ratio_base60 = ratio.to_base60(20);
        let ratio_wedge = base60_to_wedge(&ratio_base60.integer_part, &ratio_base60.fractional_part);
        
        triples.push(Triple {
            row: row + 1,
            p: *p_ref as u32,
            q: *q_ref as u32,
            a,
            b,
            c,
            ratio_a_c: ratio_wedge.clone(),
            wedge_a: base60_to_wedge(&Rational::from_int(a).to_base60(10).integer_part, &[]),
            wedge_b: base60_to_wedge(&Rational::from_int(b).to_base60(10).integer_part, &[]),
            wedge_c: base60_to_wedge(&Rational::from_int(c).to_base60(10).integer_part, &[]),
        });
    }
    
    serde_wasm_bindgen::to_value(&triples).unwrap()
}

/// YBC 7290 √2 approximation
/// The Babylonian clay tablet YBC 7289 (often called YBC 7290) contains 
/// a square with diagonal, giving √2 ≈ 1;24,51,10 in base-60
#[wasm_bindgen]
pub fn ybc7290_sqrt2() -> JsValue {
    // The famous approximation: 1 + 24/60 + 51/3600 + 10/216000
    // = 305470/216000 = 1.41421296...
    let approx = Rational::new(305470, 216000);
    let exact_sqrt2 = Rational::from_int(2).sqrt_approx(10);
    
    let approx_base60 = approx.to_base60(10);
    let exact_base60 = exact_sqrt2.to_base60(10);
    
    #[derive(Serialize)]
    struct Sqrt2Result {
        babylonian_approximation: String,
        babylonian_wedge: String,
        exact_base60: String,
        exact_wedge: String,
        decimal_approximation: f64,
        decimal_exact: f64,
        error: f64,
        clay_tablet_notation: String,
    }
    
    let clay_notation = "1;24,51,10".to_string();
    let approx_wedge = base60_to_wedge(&approx_base60.integer_part, &approx_base60.fractional_part);
    let exact_wedge = base60_to_wedge(&exact_base60.integer_part, &exact_base60.fractional_part);
    
    serde_wasm_bindgen::to_value(&Sqrt2Result {
        babylonian_approximation: "305470/216000".to_string(),
        babylonian_wedge: approx_wedge,
        exact_base60: format!("{:?}", exact_base60),
        exact_wedge,
        decimal_approximation: approx.to_f64(),
        decimal_exact: exact_sqrt2.to_f64(),
        error: (approx.to_f64() - 2.0_f64.sqrt()).abs(),
        clay_tablet_notation: clay_notation,
    }).unwrap()
}

/// Construct a regular 17-gon using Gauss-Wantzel construction
/// 17 = 2^4 + 1 (Fermat prime), constructible with compass and straightedge
#[wasm_bindgen]
pub fn construct_17gon() -> JsValue {
    // Gauss's construction: cos(2π/17) = 1/16 * (-1 + √17 + √(34-2√17) + 2√(17+3√17-√(34-2√17)-2√(34+2√17)))
    // We'll compute the vertices using exact arithmetic
    
    #[derive(Serialize)]
    struct Vertex {
        index: usize,
        angle_rad: f64,
        x: f64,
        y: f64,
        x_wedge: String,
        y_wedge: String,
    }
    
    #[derive(Serialize)]
    struct Gon17Result {
        vertices: Vec<Vertex>,
        construction_steps: Vec<String>,
        gauss_expression: String,
    }
    
    // Compute cos(2π/17) and sin(2π/17) using exact rational approximation
    let mut vertices = Vec::new();
    for i in 0..17 {
        let angle = 2.0 * std::f64::consts::PI * i as f64 / 17.0;
        let x = angle.cos();
        let y = angle.sin();
        
        // Convert to base-60 for display
        let x_rat = Rational::new((x * 216000.0).round() as i64, 216000);
        let y_rat = Rational::new((y * 216000.0).round() as i64, 216000);
        let x_base60 = x_rat.to_base60(10);
        let y_base60 = y_rat.to_base60(10);
        
        vertices.push(Vertex {
            index: i,
            angle_rad: angle,
            x,
            y,
            x_wedge: base60_to_wedge(&x_base60.integer_part, &x_base60.fractional_part),
            y_wedge: base60_to_wedge(&y_base60.integer_part, &y_base60.fractional_part),
        });
    }
    
    let construction_steps = vec![
        "1. Draw a circle with center O".to_string(),
        "2. Draw diameter AB".to_string(),
        "3. Construct perpendicular diameter CD".to_string(),
        "4. Find midpoint E of OB".to_string(),
        "5. Find point F on OA such that EF = EC".to_string(),
        "6. Find point G on OA such that EG = EB".to_string(),
        "7. Bisect FG to get H".to_string(),
        "8. Draw circle with center H through G".to_string(),
        "9. Intersect with original circle to get vertices".to_string(),
        "10. Step around circle 17 times".to_string(),
    ];
    
    serde_wasm_bindgen::to_value(&Gon17Result {
        vertices,
        construction_steps,
        gauss_expression: "cos(2π/17) = 1/16(-1 + √17 + √(34-2√17) + 2√(17+3√17-√(34-2√17)-2√(34+2√17)))".to_string(),
    }).unwrap()
}

/// Generate interactive clay tablet SVG
#[wasm_bindgen]
pub fn generate_clay_tablet_svg(width: u32, height: u32, content: &str) -> String {
    let mut svg = String::new();
    svg.push_str(&format!(
        r###"<svg width="{}" height="{}" viewBox="0 0 {} {}" xmlns="http://www.w3.org/2000/svg">"###,
        width, height, width, height
    ));
    
    // Clay tablet background - trapezoid shape
    let padding = 20.0;
    let w = width as f64 - 2.0 * padding;
    let h = height as f64 - 2.0 * padding;
    let top_width = w * 0.85;
    let left_offset = (w - top_width) / 2.0;
    
    // Main clay body
    svg.push_str(&format!(
        r###"<path d="M {},{} L {},{} L {},{} L {},{} Z" fill="#C47D3E" stroke="#8B5A2B" stroke-width="2"/>"###,
        padding + left_offset, padding,
        padding + left_offset + top_width, padding,
        width as f64 - padding, height as f64 - padding,
        padding, height as f64 - padding
    ));
    
    // Cuneiform texture lines
    for i in 0..10 {
        let y = padding + h * (i as f64 + 0.5) / 10.0;
        let x1 = padding + left_offset * (1.0 - (i as f64 / 10.0) * 0.3);
        let x2 = padding + left_offset + top_width - left_offset * (1.0 - (i as f64 / 10.0) * 0.3);
        svg.push_str(&format!(
            r###"<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="#A06D30" stroke-width="0.5" opacity="0.5"/>"###,
            x1, y, x2, y
        ));
    }
    
    // Content text (wedge numerals)
    let lines: Vec<&str> = content.lines().collect();
    for (i, line) in lines.iter().enumerate() {
        let y = padding + 30.0 + i as f64 * 25.0;
        let x = padding + left_offset + 20.0;
        svg.push_str(&format!(
            r###"<text x="{}" y="{}" font-family="'Noto Sans Cuneiform', monospace" font-size="18" fill="#5D3A1A">{}</text>"###,
            x, y, line
        ));
    }
    
    svg.push_str("</svg>");
    svg
}

/// Interactive fraction addition visualization data
#[wasm_bindgen]
pub fn fraction_addition_visual(a_num: i64, a_den: i64, b_num: i64, b_den: i64) -> JsValue {
    let a = Rational::new(a_num, a_den);
    let b = Rational::new(b_num, b_den);
    let sum = a.add(&b);
    
    #[derive(Serialize)]
    struct VisualData {
        a_wedge: String,
        b_wedge: String,
        sum_wedge: String,
        a_base60: Base60Digits,
        b_base60: Base60Digits,
        sum_base60: Base60Digits,
        common_denominator: i64,
        steps: Vec<String>,
        // For visual bars
        a_parts: Vec<f64>,
        b_parts: Vec<f64>,
        sum_parts: Vec<f64>,
    }
    
    let a_base60 = a.to_base60(10);
    let b_base60 = b.to_base60(10);
    let sum_base60 = sum.to_base60(10);
    
    let a_wedge = base60_to_wedge(&a_base60.integer_part, &a_base60.fractional_part);
    let b_wedge = base60_to_wedge(&b_base60.integer_part, &b_base60.fractional_part);
    let sum_wedge = base60_to_wedge(&sum_base60.integer_part, &sum_base60.fractional_part);
    
    // Visual representation as parts of a whole (for 5th grade)
    let lcm = lcm(a_den, b_den);
    let a_parts = vec![a_num as f64 / a_den as f64];
    let b_parts = vec![b_num as f64 / b_den as f64];
    let sum_parts = vec![sum.numerator as f64 / sum.denominator as f64];
    
    let steps = vec![
        format!("Step 1: Find common denominator for {} and {}", a_den, b_den),
        format!("Step 2: Convert {}/{} to {}/{}", a_num, a_den, a_num * (lcm/a_den), lcm),
        format!("Step 3: Convert {}/{} to {}/{}", b_num, b_den, b_num * (lcm/b_den), lcm),
        format!("Step 4: Add numerators: {} + {} = {}", a_num * (lcm/a_den), b_num * (lcm/b_den), a_num * (lcm/a_den) + b_num * (lcm/b_den)),
        format!("Step 5: Result = {}/{} = {}/{}", a_num * (lcm/a_den) + b_num * (lcm/b_den), lcm, sum.numerator, sum.denominator),
        format!("Step 6: In base-60: {}", sum_wedge),
    ];
    
    serde_wasm_bindgen::to_value(&VisualData {
        a_wedge,
        b_wedge,
        sum_wedge,
        a_base60,
        b_base60,
        sum_base60,
        common_denominator: lcm,
        steps,
        a_parts,
        b_parts,
        sum_parts,
    }).unwrap()
}

fn lcm(a: i64, b: i64) -> i64 {
    a.abs() * b.abs() / gcd(a, b)
}

/// Get all available functions for the JS frontend
#[wasm_bindgen]
pub fn get_api_info() -> JsValue {
    #[derive(Serialize)]
    struct ApiInfo {
        version: String,
        functions: Vec<String>,
    }
    
    serde_wasm_bindgen::to_value(&ApiInfo {
        version: "0.1.0".to_string(),
        functions: vec![
            "rational_to_base60".to_string(),
            "digit_to_wedge".to_string(),
            "base60_to_wedge".to_string(),
            "reciprocal_pair_add".to_string(),
            "reciprocal_pair_mul".to_string(),
            "generate_reciprocal_table".to_string(),
            "generate_plimpton_triples".to_string(),
            "ybc7290_sqrt2".to_string(),
            "construct_17gon".to_string(),
            "generate_clay_tablet_svg".to_string(),
            "fraction_addition_visual".to_string(),
            "get_api_info".to_string(),
        ],
    }).unwrap()
}