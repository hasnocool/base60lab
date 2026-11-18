import React, { useState, useEffect } from 'react';
import { 
  loadWasm, 
  reciprocalPairMul,
  generateReciprocalTable,
  generatePlimptonTriples,
  ybc7290Sqrt2,
  construct17gon,
  generateClayTabletSvg,
  fractionAdditionVisual,
} from './wasm';
import type { 
  ReciprocalEntry, 
  FractionResult,
  PlimptonTriple,
  Sqrt2Result,
  Gon17Result,
  Vertex,
  VisualData 
} from './types';

type Tab = 'home' | 'fractions' | 'reciprocals' | 'plimpton' | 'sqrt2' | 'polygon' | 'tablet';

function HomeTab() {
  return (
    <div className="tab-panel">
      <section className="section">
        <h2><span className="wedge">𒌋</span> Welcome to the Babylonian Fraction Arithmetic Visualizer</h2>
        <p style={{fontSize: '1.1rem', lineHeight: 1.8, marginBottom: '1.5rem'}}>
          Explore ancient Babylonian mathematics through interactive visualizations. 
          The Babylonians used base-60 (sexagesimal) arithmetic with exact rational numbers — 
          no floating-point approximations, just pure mathematics as they practiced it 4000 years ago.
        </p>
        <div className="card-grid">
          <div className="card">
            <h3>📐 Fraction Arithmetic</h3>
            <p>Add and multiply fractions using the reciprocal pair method. Visualize with fraction bars and base-60 wedge numerals.</p>
          </div>
          <div className="card">
            <h3>📊 Reciprocal Tables</h3>
            <p>Generate Babylonian-style reciprocal tables for regular numbers (5-smooth: 2ᵃ×3ᵇ×5ᶜ). See which fractions terminate in base-60.</p>
          </div>
          <div className="card">
            <h3>📜 Plimpton 322</h3>
            <p>Reconstruct the famous 15 Pythagorean triples from the Plimpton 322 clay tablet using the reciprocal-pair method.</p>
          </div>
          <div className="card">
            <h3>√2 Approximation</h3>
            <p>Explore the YBC 7290 tablet's remarkable √2 ≈ 1;24,51,10 (base-60) — accurate to 6 decimal places!</p>
          </div>
          <div className="card">
            <h3>⬟ 17-gon Construction</h3>
            <p>Visualize Gauss's construction of the regular 17-gon — a Fermat prime constructible with compass and straightedge.</p>
          </div>
          <div className="card">
            <h3>🪨 Clay Tablet</h3>
            <p>Create your own interactive clay tablet with Babylonian wedge numerals. Write like a scribe!</p>
          </div>
        </div>
      </section>

      <section className="section">
        <h2><span className="wedge">𒁹</span> Quick Start: Fraction Addition</h2>
        <div className="fraction-visual">
          <div className="input-group">
            <label>First fraction:</label>
            <input type="number" value={1} readOnly style={{width: '50px'}} /> /
            <input type="number" value={3} readOnly style={{width: '50px'}} />
            <span style={{margin: '0 1rem'}}>=</span>
            <input type="number" value={1} readOnly style={{width: '50px'}} /> /
            <input type="number" value={4} readOnly style={{width: '50px'}} />
          </div>
          <div className="wedge-display">𒁹 ; 𒁹𒁹𒁹  +  𒁹 ; 𒁹𒁹𒁹𒁹  =  𒁹 ; 𒁹𒁹𒁹𒁹𒁹</div>
          <div className="base60-display">Base-60: 0;20 + 0;15 = 0;35</div>
          <div className="base60-display">Decimal: 1/3 + 1/4 = 7/12 ≈ 0.58333...</div>
        </div>
      </section>
    </div>
  );
}

function FractionsTab({ 
  fracA, setFracA, fracB, setFracB, addResult, handleFractionAdd,
  mulFracA, setMulFracA, mulFracB, setMulFracB, mulResult, handleFractionMul 
}: any) {
  return (
    <div className="tab-panel">
      <section className="section">
        <h2><span className="wedge">𒌋</span> Fraction Addition (Reciprocal Pair Method)</h2>
        <p>Babylonians used reciprocal tables: to divide by n, multiply by its reciprocal 1/n. 
        Addition: a/b + c/d = (ad + bc)/bd. Visualize with fraction bars!</p>
        
        <div className="card-grid">
          <div className="card">
            <h3>First Fraction</h3>
            <div className="input-group">
              <label>Numerator:</label>
              <input 
                type="number" 
                value={fracA.num} 
                onChange={(e) => setFracA({...fracA, num: parseInt(e.target.value) || 1})}
                min={-100} max={100}
              />
              <label>Denominator:</label>
              <input 
                type="number" 
                value={fracA.den} 
                onChange={(e) => setFracA({...fracA, den: parseInt(e.target.value) || 1})}
                min={1} max={100}
              />
            </div>
            <div className="wedge-display">{addResult?.a_wedge || '𒁹 ; 𒁹𒁹𒁹'}</div>
            <div className="base60-display">1/3 = 0;20 (base-60)</div>
          </div>
          
          <div className="card">
            <h3>Second Fraction</h3>
            <div className="input-group">
              <label>Numerator:</label>
              <input 
                type="number" 
                value={fracB.num} 
                onChange={(e) => setFracB({...fracB, num: parseInt(e.target.value) || 1})}
                min={-100} max={100}
              />
              <label>Denominator:</label>
              <input 
                type="number" 
                value={fracB.den} 
                onChange={(e) => setFracB({...fracB, den: parseInt(e.target.value) || 1})}
                min={1} max={100}
              />
            </div>
            <div className="wedge-display">{addResult?.b_wedge || '𒁹 ; 𒁹𒁹𒁹𒁹'}</div>
            <div className="base60-display">1/4 = 0;15 (base-60)</div>
          </div>
        </div>

        <button className="btn btn-primary" onClick={handleFractionAdd} style={{marginTop: '1rem'}}>
          Calculate Sum
        </button>

        {addResult && (
          <div className="card" style={{marginTop: '1rem'}}>
            <h3>Result: {fracA.num}/{fracA.den} + {fracB.num}/{fracB.den} = {addResult.sum_wedge}</h3>
            <div className="fraction-visual">
              <div className="fraction-bar">
                <div className="fraction-fill fill-a" style={{width: `${(fracA.num/fracA.den)*100}%`}}>
                  {fracA.num}/{fracA.den}
                </div>
              </div>
              <div className="fraction-bar">
                <div className="fraction-fill fill-b" style={{width: `${(fracB.num/fracB.den)*100}%`}}>
                  {fracB.num}/{fracB.den}
                </div>
              </div>
              <div className="fraction-bar">
                <div className="fraction-fill fill-sum" style={{width: `${(addResult.sum_parts[0])*100}%`}}>
                  {addResult.sum_parts[0].toFixed(4)} = {addResult.numerator}/{addResult.denominator}
                </div>
              </div>
              <div className="legend">
                <div className="legend-item"><div className="legend-color fill-a"></div> {fracA.num}/{fracA.den}</div>
                <div className="legend-item"><div className="legend-color fill-b"></div> {fracB.num}/{fracB.den}</div>
                <div className="legend-item"><div className="legend-color fill-sum"></div> Sum</div>
              </div>
            </div>
            <div className="wedge-display">{addResult.sum_wedge}</div>
            <div className="base60-display">Common denominator: {addResult.common_denominator}</div>
            <h4>Steps:</h4>
            <ul className="steps-list">
              {addResult.steps.map((step: string, i: number) => <li key={i}>{step}</li>)}
            </ul>
          </div>
        )}
      </section>

      <section className="section">
        <h2><span className="wedge">𒁹</span> Fraction Multiplication</h2>
        <p>Multiplication: a/b × c/d = ac/bd. Babylonians would look up reciprocals and multiply.</p>
        
        <div className="card-grid">
          <div className="card">
            <h3>First Fraction</h3>
            <div className="input-group">
              <label>Numerator:</label>
              <input 
                type="number" 
                value={mulFracA.num} 
                onChange={(e) => setMulFracA({...mulFracA, num: parseInt(e.target.value) || 1})}
                min={-100} max={100}
              />
              <label>Denominator:</label>
              <input 
                type="number" 
                value={mulFracA.den} 
                onChange={(e) => setMulFracA({...mulFracA, den: parseInt(e.target.value) || 1})}
                min={1} max={100}
              />
            </div>
          </div>
          <div className="card">
            <h3>Second Fraction</h3>
            <div className="input-group">
              <label>Numerator:</label>
              <input 
                type="number" 
                value={mulFracB.num} 
                onChange={(e) => setMulFracB({...mulFracB, num: parseInt(e.target.value) || 1})}
                min={-100} max={100}
              />
              <label>Denominator:</label>
              <input 
                type="number" 
                value={mulFracB.den} 
                onChange={(e) => setMulFracB({...mulFracB, den: parseInt(e.target.value) || 1})}
                min={1} max={100}
              />
            </div>
          </div>
        </div>

        <button className="btn btn-primary" onClick={handleFractionMul} style={{marginTop: '1rem'}}>
          Calculate Product
        </button>

        {mulResult && (
          <div className="card" style={{marginTop: '1rem'}}>
            <h3>Result: {mulFracA.num}/{mulFracA.den} × {mulFracB.num}/{mulFracB.den} = {mulResult.numerator}/{mulResult.denominator}</h3>
            <div className="wedge-display">{mulResult.wedge}</div>
            <div className="base60-display">{mulResult.base60.integer_part.join(',')};{mulResult.base60.fractional_part.join(',')}</div>
            <h4>Steps:</h4>
            <ul className="steps-list">
              {mulResult.steps.map((step: string, i: number) => <li key={i}>{step}</li>)}
            </ul>
          </div>
        )}
      </section>
    </div>
  );
}

function ReciprocalsTab({ reciprocalTable, reciprocalLimit, setReciprocalLimit }: any) {
  return (
    <div className="tab-panel">
      <section className="section">
        <h2><span className="wedge">𒌋</span> Babylonian Reciprocal Tables</h2>
        <p>Regular numbers (5-smooth: 2ᵃ×3ᵇ×5ᶜ) have terminating reciprocals in base-60. 
        Babylonians pre-computed these for division: to divide by n, multiply by 1/n.</p>
        
        <div className="input-group">
          <label>Limit:</label>
          <input 
            type="number" 
            value={reciprocalLimit} 
            onChange={(e) => setReciprocalLimit(parseInt(e.target.value) || 60)}
            min={10} max={360}
          />
          <button className="btn btn-secondary" onClick={() => window.location.reload()}>
            Generate Table
          </button>
        </div>

        <div className="table-container" style={{marginTop: '1rem'}}>
          <table>
            <thead>
              <tr>
                <th>n</th>
                <th>1/n (decimal)</th>
                <th>Base-60</th>
                <th>Wedge Numerals</th>
                <th>Terminates</th>
              </tr>
            </thead>
            <tbody>
              {reciprocalTable.map((entry: ReciprocalEntry) => (
                <tr key={entry.n}>
                  <td><strong>{entry.n}</strong></td>
                  <td>1/{entry.n}</td>
                  <td className="base60-display">
                    {entry.base60.integer_part.join(',')};{entry.base60.fractional_part.join(',')}
                    {entry.base60.is_repeating ? ` (repeats at ${entry.base60.repeating_start})` : ''}
                  </td>
                  <td className="wedge-cell">{entry.wedge}</td>
                  <td>{entry.terminates ? '✅ Yes' : '❌ No'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

function PlimptonTab({ plimptonTriples }: any) {
  return (
    <div className="tab-panel">
      <section className="section">
        <h2><span className="wedge">𒌋</span> Plimpton 322: 15 Pythagorean Triples</h2>
        <p>The famous clay tablet Plimpton 322 (c. 1800 BCE) contains 15 rows of Pythagorean triples 
        generated by the reciprocal-pair method: (p, q) → (p²+q², p²-q², 2pq).</p>
        
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Row</th>
                <th>p</th>
                <th>q</th>
                <th>a = p²+q² (hypotenuse)</th>
                <th>b = p²-q² (long leg)</th>
                <th>c = 2pq (short leg)</th>
                <th>a/c ratio (base-60)</th>
              </tr>
            </thead>
            <tbody>
              {plimptonTriples.map((triple: PlimptonTriple) => (
                <tr key={triple.row}>
                  <td>{triple.row}</td>
                  <td>{triple.p}</td>
                  <td>{triple.q}</td>
                  <td>{triple.a} <div className="wedge-cell">{triple.wedge_a}</div></td>
                  <td>{triple.b} <div className="wedge-cell">{triple.wedge_b}</div></td>
                  <td>{triple.c} <div className="wedge-cell">{triple.wedge_c}</div></td>
                  <td className="wedge-cell">{triple.ratio_a_c}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="card" style={{marginTop: '1.5rem'}}>
          <h3>How It Works (Reciprocal-Pair Method)</h3>
          <ul className="steps-list">
            <li>Choose regular numbers p {" > "} q (from reciprocal table)</li>
            <li>Compute: a = p² + q², b = p² - q², c = 2pq</li>
            <li>Then a² = b² + c² (Pythagorean triple!)</li>
            <li>The ratio a/c = (p/q + q/p)/2 in base-60</li>
          </ul>
        </div>
      </section>
    </div>
  );
}

function Sqrt2Tab({ sqrt2Result }: any) {
  return (
    <div className="tab-panel">
      <section className="section">
        <h2><span className="wedge">𒌋</span> YBC 7290: The √2 Approximation</h2>
        <p>The Yale Babylonian Collection tablet YBC 7289 (often called YBC 7290) shows a square 
        with its diagonal, giving the remarkable approximation √2 ≈ 1;24,51,10 (base-60).</p>
        
        {sqrt2Result && (
          <div className="card-grid">
            <div className="card">
              <h3>Babylonian Value</h3>
              <div className="wedge-display">{sqrt2Result.babylonian_wedge}</div>
              <div className="base60-display">1;24,51,10 (base-60)</div>
              <div className="base60-display">Fraction: {sqrt2Result.babylonian_approximation}</div>
              <div className="base60-display">Decimal: {sqrt2Result.decimal_approximation.toFixed(10)}</div>
            </div>
            
            <div className="card">
              <h3>Exact √2</h3>
              <div className="wedge-display">{sqrt2Result.exact_wedge}</div>
              <div className="base60-display">Decimal: {sqrt2Result.decimal_exact.toFixed(10)}</div>
            </div>
            
            <div className="card">
              <h3>Accuracy</h3>
              <div style={{fontSize: '2rem', fontWeight: 'bold', color: 'var(--accent)'}}>
                Error: {sqrt2Result.error.toExponential(3)}
              </div>
              <div className="base60-display">Accurate to 6 decimal places!</div>
              <div className="base60-display">Clay tablet notation: {sqrt2Result.clay_tablet_notation}</div>
            </div>
          </div>
        )}
        
        <div className="card" style={{marginTop: '1.5rem'}}>
          <h3>Historical Context</h3>
          <ul className="steps-list">
            <li>Tablet YBC 7289/7290 dates to c. 1800–1600 BCE (Old Babylonian period)</li>
            <li>Shows a square of side 30 with diagonal 42;25,35</li>
            <li>30 × √2 ≈ 30 × 1;24,51,10 = 42;25,30 (tablet shows 42;25,35)</li>
            <li>This is the most accurate √2 approximation from antiquity</li>
            <li>Achieved using Babylonian base-60 arithmetic, likely via iterative method</li>
          </ul>
        </div>
      </section>
    </div>
  );
}

function PolygonTab({ gon17Result, selectedVertex, setSelectedVertex }: any) {
  const canvasRef = React.useRef<HTMLCanvasElement>(null);
  
  React.useEffect(() => {
    if (!canvasRef.current || !gon17Result) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d')!;
    const size = Math.min(canvas.width, canvas.height);
    const center = size / 2;
    const radius = size * 0.4;
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw circle
    ctx.beginPath();
    ctx.arc(center, center, radius, 0, 2 * Math.PI);
    ctx.strokeStyle = '#8B5A2B';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Draw vertices and polygon
    const vertices = gon17Result.vertices;
    
    // Draw polygon edges
    ctx.beginPath();
    vertices.forEach((v: Vertex, i: number) => {
      const x = center + radius * Math.cos(v.angle_rad);
      const y = center + radius * Math.sin(v.angle_rad);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.closePath();
    ctx.strokeStyle = '#C47D3E';
    ctx.lineWidth = 1.5;
    ctx.stroke();
    
    // Draw vertices
    vertices.forEach((v: Vertex, i: number) => {
      const x = center + radius * Math.cos(v.angle_rad);
      const y = center + radius * Math.sin(v.angle_rad);
      
      ctx.beginPath();
      ctx.arc(x, y, selectedVertex?.index === i ? 8 : 5, 0, 2 * Math.PI);
      ctx.fillStyle = selectedVertex?.index === i ? '#C0392B' : '#27ae60';
      ctx.fill();
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 2;
      ctx.stroke();
    });
    
    // Draw center
    ctx.beginPath();
    ctx.arc(center, center, 4, 0, 2 * Math.PI);
    ctx.fillStyle = '#8B5A2B';
    ctx.fill();
  }, [gon17Result, selectedVertex]);
  
  return (
    <div className="tab-panel">
      <section className="section">
        <h2><span className="wedge">𒌋</span> Regular 17-gon (Gauss Construction)</h2>
        <p>17 = 2⁴ + 1 is a Fermat prime. Gauss proved at age 19 that a regular 17-gon is constructible 
        with compass and straightedge. The construction uses nested square roots.</p>
        
        <div style={{textAlign: 'center', marginBottom: '1rem'}}>
          <canvas 
            ref={canvasRef} 
            className="polygon-canvas"
            width={500} 
            height={500}
            onClick={(e) => {
              if (!gon17Result || !canvasRef.current) return;
              const canvas = canvasRef.current;
              const rect = canvas.getBoundingClientRect();
              const x = e.clientX - rect.left - canvas.width / 2;
              const y = e.clientY - rect.top - canvas.height / 2;
              const angle = Math.atan2(y, x);
              const index = Math.round((angle + Math.PI) / (2 * Math.PI) * 17) % 17;
              setSelectedVertex(gon17Result.vertices[index]);
            }}
          />
        </div>
        
        {selectedVertex && (
          <div className="card" style={{maxWidth: '500px', margin: '0 auto 1rem'}}>
            <h3>Vertex {selectedVertex.index}</h3>
            <div className="wedge-display">
              x: {selectedVertex.x_wedge}<br/>
              y: {selectedVertex.y_wedge}
            </div>
            <div className="base60-display">
              Angle: {(selectedVertex.angle_rad * 180 / Math.PI).toFixed(2)}°
            </div>
            <div className="base60-display">
              Cartesian: ({selectedVertex.x.toFixed(4)}, {selectedVertex.y.toFixed(4)})
            </div>
          </div>
        )}
        
        <div className="card">
          <h3>Gauss's Expression for cos(2π/17)</h3>
          <div className="base60-display" style={{fontSize: '0.875rem', wordBreak: 'break-all'}}>
            {gon17Result?.gauss_expression}
          </div>
        </div>
        
        <div className="card">
          <h3>Construction Steps</h3>
          <ul className="steps-list">
            {gon17Result?.construction_steps.map((step: string, i: number) => <li key={i}>{step}</li>)}
          </ul>
        </div>
      </section>
    </div>
  );
}

function TabletTab({ tabletContent, setTabletContent, tabletSvg, handleGenerateTablet }: any) {
  return (
    <div className="tab-panel">
      <section className="section">
        <h2><span className="wedge">𒌋</span> Interactive Clay Tablet</h2>
        <p>Write like a Babylonian scribe! Enter wedge numerals (one per line) and generate a clay tablet SVG.</p>
        
        <div className="card">
          <h3>Tablet Content</h3>
          <textarea
            value={tabletContent}
            onChange={(e) => setTabletContent(e.target.value)}
            rows={8}
            style={{
              width: '100%',
              padding: '1rem',
              border: '2px solid rgba(140, 90, 43, 0.2)',
              borderRadius: '8px',
              fontFamily: "'Noto Sans Cuneiform', monospace",
              fontSize: '1.25rem',
              lineHeight: '2',
              background: '#fdfbf7',
              color: '#5D3A1A',
              resize: 'vertical',
            }}
            placeholder="Enter wedge numerals, one per line. Example:
𒁹 ; 𒁹𒁹𒁹
𒁹 ; 𒁹𒁹𒁹𒁹
𒁹 ; 𒁹𒁹𒁹𒁹𒁹
𒌋𒁹 ; 𒌋𒁹
1/3 + 1/4 = 7/12"
          />
          <button className="btn btn-primary" onClick={handleGenerateTablet} style={{marginTop: '1rem'}}>
            Generate Tablet
          </button>
        </div>
        
        {tabletSvg && (
          <div className="card" style={{marginTop: '1.5rem'}}>
            <h3>Generated Tablet</h3>
            <div style={{textAlign: 'center'}}>
              <div dangerouslySetInnerHTML={{__html: tabletSvg}} />
            </div>
          </div>
        )}
        
        <div className="card" style={{marginTop: '1.5rem'}}>
          <h3>Wedge Numeral Reference</h3>
          <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(120px, 1fr))', gap: '0.5rem'}}>
            {Array.from({length: 10}, (_, i) => i + 1).map(n => (
              <div key={n} style={{padding: '0.5rem', background: 'var(--white)', borderRadius: '8px', border: '1px solid rgba(140, 90, 43, 0.2)', textAlign: 'center'}}>
                <div className="wedge-display" style={{fontSize: '1.5rem', padding: '0.5rem'}}>{Array(n).fill('𒁹').join('')}</div>
                <div style={{fontSize: '0.75rem', color: 'var(--text-light)'}}>{n}</div>
              </div>
            ))}
            {Array.from({length: 5}, (_, i) => (i + 1) * 10).map(n => (
              <div key={n} style={{padding: '0.5rem', background: 'var(--white)', borderRadius: '8px', border: '1px solid rgba(140, 90, 43, 0.2)', textAlign: 'center'}}>
                <div className="wedge-display" style={{fontSize: '1.5rem', padding: '0.5rem'}}>{Array(n/10).fill('𒌋').join('')}</div>
                <div style={{fontSize: '0.75rem', color: 'var(--text-light)'}}>{n}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('home');
  const [wasmLoaded, setWasmLoaded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fraction addition state
  const [fracA, setFracA] = useState({ num: 1, den: 3 });
  const [fracB, setFracB] = useState({ num: 1, den: 4 });
  const [addResult, setAddResult] = useState<VisualData | null>(null);

  // Fraction multiplication state
  const [mulFracA, setMulFracA] = useState({ num: 2, den: 5 });
  const [mulFracB, setMulFracB] = useState({ num: 3, den: 7 });
  const [mulResult, setMulResult] = useState<FractionResult | null>(null);

  // Reciprocal table state
  const [reciprocalTable, setReciprocalTable] = useState<ReciprocalEntry[]>([]);
  const [reciprocalLimit, setReciprocalLimit] = useState(60);

  // Plimpton 322 state
  const [plimptonTriples, setPlimptonTriples] = useState<PlimptonTriple[]>([]);

  // YBC 7290 √2 state
  const [sqrt2Result, setSqrt2Result] = useState<Sqrt2Result | null>(null);

  // 17-gon state
  const [gon17Result, setGon17Result] = useState<Gon17Result | null>(null);
  const [selectedVertex, setSelectedVertex] = useState<Vertex | null>(null);

  // Clay tablet state
  const [tabletContent, setTabletContent] = useState('');
  const [tabletSvg, setTabletSvg] = useState('');

  const loadAllData = async () => {
    try {
      const [reciprocals, plimpton, sqrt2, gon17] = await Promise.all([
        generateReciprocalTable(reciprocalLimit),
        generatePlimptonTriples(),
        ybc7290Sqrt2(),
        construct17gon(),
      ]);
      setReciprocalTable(reciprocals);
      setPlimptonTriples(plimpton);
      setSqrt2Result(sqrt2);
      setGon17Result(gon17);
    } catch (err) {
      console.error('Failed to load data:', err);
    }
  };

  useEffect(() => {
    const initWasm = async () => {
      setLoading(true);
      setError(null);
      try {
        await loadWasm();
        setWasmLoaded(true);
        await loadAllData();
      } catch (err) {
        setError('Failed to load WASM module. Make sure to build it first with `wasm-pack build`.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    initWasm();
  }, []);

  const handleFractionAdd = async () => {
    try {
      const result = await fractionAdditionVisual(fracA.num, fracA.den, fracB.num, fracB.den);
      setAddResult(result);
    } catch (err) {
      console.error('Fraction addition failed:', err);
    }
  };

  const handleFractionMul = async () => {
    try {
      const result = await reciprocalPairMul(mulFracA.num, mulFracA.den, mulFracB.num, mulFracB.den);
      setMulResult(result);
    } catch (err) {
      console.error('Fraction multiplication failed:', err);
    }
  };

  const handleGenerateTablet = async () => {
    try {
      const svg = await generateClayTabletSvg(600, 400, tabletContent);
      setTabletSvg(svg);
    } catch (err) {
      console.error('Tablet generation failed:', err);
    }
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'home':
        return <HomeTab />;
      case 'fractions':
        return (
          <FractionsTab 
            fracA={fracA} setFracA={setFracA} 
            fracB={fracB} setFracB={setFracB} 
            addResult={addResult} handleFractionAdd={handleFractionAdd}
            mulFracA={mulFracA} setMulFracA={setMulFracA}
            mulFracB={mulFracB} setMulFracB={setMulFracB}
            mulResult={mulResult} handleFractionMul={handleFractionMul}
          />
        );
      case 'reciprocals':
        return <ReciprocalsTab reciprocalTable={reciprocalTable} reciprocalLimit={reciprocalLimit} setReciprocalLimit={setReciprocalLimit} />;
      case 'plimpton':
        return <PlimptonTab plimptonTriples={plimptonTriples} />;
      case 'sqrt2':
        return <Sqrt2Tab sqrt2Result={sqrt2Result} />;
      case 'polygon':
        return <PolygonTab gon17Result={gon17Result} selectedVertex={selectedVertex} setSelectedVertex={setSelectedVertex} />;
      case 'tablet':
        return <TabletTab tabletContent={tabletContent} setTabletContent={setTabletContent} tabletSvg={tabletSvg} handleGenerateTablet={handleGenerateTablet} />;
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <h1>
            <span className="wedge">𒁹</span>
            Babylonian Fraction Arithmetic Visualizer
          </h1>
          <nav className="nav-tabs">
            <button 
              className={`nav-tab ${activeTab === 'home' ? 'active' : ''}`}
              onClick={() => setActiveTab('home')}
            >
              Home
            </button>
            <button 
              className={`nav-tab ${activeTab === 'fractions' ? 'active' : ''}`}
              onClick={() => setActiveTab('fractions')}
            >
              Fractions
            </button>
            <button 
              className={`nav-tab ${activeTab === 'reciprocals' ? 'active' : ''}`}
              onClick={() => setActiveTab('reciprocals')}
            >
              Reciprocals
            </button>
            <button 
              className={`nav-tab ${activeTab === 'plimpton' ? 'active' : ''}`}
              onClick={() => setActiveTab('plimpton')}
            >
              Plimpton 322
            </button>
            <button 
              className={`nav-tab ${activeTab === 'sqrt2' ? 'active' : ''}`}
              onClick={() => setActiveTab('sqrt2')}
            >
              YBC 7290 √2
            </button>
            <button 
              className={`nav-tab ${activeTab === 'polygon' ? 'active' : ''}`}
              onClick={() => setActiveTab('polygon')}
            >
              17-gon
            </button>
            <button 
              className={`nav-tab ${activeTab === 'tablet' ? 'active' : ''}`}
              onClick={() => setActiveTab('tablet')}
            >
              Clay Tablet
            </button>
          </nav>
        </div>
      </header>

      <main className="main">
        {error && (
          <div className="section" style={{ borderColor: 'var(--accent)', background: '#fdf2f2' }}>
            <h2>⚠️ Error</h2>
            <p>{error}</p>
            <button className="btn btn-primary" onClick={() => window.location.reload()}>Retry</button>
          </div>
        )}

        {loading && (
          <div className="section" style={{ textAlign: 'center' }}>
            <p>Loading Babylonian mathematics...</p>
          </div>
        )}

        {wasmLoaded && !loading && !error && renderTabContent()}
      </main>

      <footer className="footer">
        <div className="footer-content">
          <p>Babylonian Fraction Arithmetic Visualizer — Built with Rust, WebAssembly & React</p>
          <p>Base-60 exact rational arithmetic • 5th Grade Curriculum Pilot • <a href="https://github.com" target="_blank" rel="noopener" style={{color: 'var(--clay-light)'}}>Open Source</a></p>
        </div>
      </footer>
    </div>
  );
}

export default App;