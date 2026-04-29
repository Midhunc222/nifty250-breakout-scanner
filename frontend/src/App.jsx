import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import {
  Activity, Play, TrendingUp, TrendingDown, RefreshCw,
  AlertCircle, Target, ShieldAlert, Clock, X, Star, Zap, Award
} from 'lucide-react';
import { createChart } from 'lightweight-charts';

// ─── Chart Component ────────────────────────────────────────────────────────
const LightweightChart = ({ data, lines, className = "chart-container" }) => {
  const containerRef = useRef();
  const chartRef = useRef();

  useEffect(() => {
    if (!containerRef.current || !data || data.length === 0) return;

    const chart = createChart(containerRef.current, {
      layout: { background: { type: 'solid', color: 'transparent' }, textColor: '#94a3b8' },
      grid: {
        vertLines: { color: 'rgba(255,255,255,0.04)' },
        horzLines: { color: 'rgba(255,255,255,0.04)' },
      },
      timeScale: { borderColor: 'rgba(255,255,255,0.1)', timeVisible: true },
      crosshair: { mode: 0 },
    });

    const candleSeries = chart.addCandlestickSeries({
      upColor: '#10b981', downColor: '#ef4444',
      borderVisible: false,
      wickUpColor: '#10b981', wickDownColor: '#ef4444',
    });

    try {
      candleSeries.setData(data);
      if (lines && lines.length > 0) {
        lines.forEach(lc => {
          if (!lc.data || lc.data.length === 0) return;
          const ls = chart.addLineSeries({
            color: lc.color,
            lineWidth: lc.lineWidth,
            crosshairMarkerVisible: false,
            lastValueVisible: false,
            priceLineVisible: false,
          });
          ls.setData(lc.data);
        });
      }
      chart.timeScale().fitContent();
    } catch (e) {
      console.error('Chart error:', e);
    }

    chartRef.current = chart;
    const onResize = () => {
      if (containerRef.current && chartRef.current)
        chartRef.current.applyOptions({ width: containerRef.current.clientWidth });
    };
    window.addEventListener('resize', onResize);
    return () => {
      window.removeEventListener('resize', onResize);
      if (chartRef.current) { chartRef.current.remove(); chartRef.current = null; }
    };
  }, [data, lines]);

  return <div ref={containerRef} className={className} />;
};

// ─── Conviction Badge ────────────────────────────────────────────────────────
const ConvictionBadge = ({ level }) => {
  const cfg = {
    High:   { bg: 'rgba(16,185,129,0.15)', color: '#10b981', border: 'rgba(16,185,129,0.4)', icon: <Zap size={12} /> },
    Medium: { bg: 'rgba(234,179,8,0.15)',  color: '#eab308', border: 'rgba(234,179,8,0.4)',  icon: <TrendingUp size={12}/> },
    Low:    { bg: 'rgba(148,163,184,0.1)', color: '#94a3b8', border: 'rgba(148,163,184,0.3)',icon: <Activity size={12}/> },
  }[level] || {};
  return (
    <span style={{
      display:'inline-flex', alignItems:'center', gap:'4px',
      background: cfg.bg, color: cfg.color,
      border: `1px solid ${cfg.border}`,
      padding: '2px 10px', borderRadius: 999,
      fontSize: '0.72rem', fontWeight: 700, letterSpacing: '0.5px',
    }}>
      {cfg.icon} {level} Conviction
    </span>
  );
};

// ─── Category color map ──────────────────────────────────────────────────────
const CATEGORY_COLORS = {
  'Volume Breakout':    '#06b6d4',
  'Cup & Handle':       '#3b82f6',
  'Channel Breakout':   '#10b981',
  'Multi-Tap':          '#f59e0b',
  'Triangle Breakout':  '#8b5cf6',
  'Downtrend Breakout': '#f97316',
};

// ─── Top Pick Hero Card ──────────────────────────────────────────────────────
const TopPickHeroCard = ({ stock, onClick }) => {
  const catColor = CATEGORY_COLORS[stock.category] || '#94a3b8';
  const risk = stock.entry - stock.sl;
  const reward = stock.target - stock.entry;
  const rr = risk > 0 ? (reward / risk).toFixed(1) : 'N/A';

  return (
    <div
      onClick={() => onClick(stock)}
      style={{
        background: `linear-gradient(135deg, rgba(18,25,38,0.95), rgba(12,18,28,0.98))`,
        border: `1px solid ${catColor}`,
        borderRadius: 16,
        padding: '1.25rem',
        cursor: 'pointer',
        position: 'relative',
        overflow: 'hidden',
        transition: 'transform 0.25s ease, box-shadow 0.25s ease',
        boxShadow: `0 0 24px ${catColor}44, 0 8px 32px rgba(0,0,0,0.5)`,
      }}
      onMouseEnter={e => {
        e.currentTarget.style.transform = 'translateY(-4px)';
        e.currentTarget.style.boxShadow = `0 0 36px ${catColor}66, 0 16px 40px rgba(0,0,0,0.6)`;
      }}
      onMouseLeave={e => {
        e.currentTarget.style.transform = 'translateY(0)';
        e.currentTarget.style.boxShadow = `0 0 24px ${catColor}44, 0 8px 32px rgba(0,0,0,0.5)`;
      }}
    >
      {/* Glow blob in background */}
      <div style={{
        position:'absolute', top:-30, right:-30,
        width:120, height:120, borderRadius:'50%',
        background: `${catColor}22`, filter:'blur(30px)', pointerEvents:'none',
      }}/>

      {/* TOP PICK pill + category */}
      <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:'0.75rem' }}>
        <span style={{
          display:'inline-flex', alignItems:'center', gap:4,
          background:`linear-gradient(135deg, ${catColor}cc, ${catColor}88)`,
          color:'#fff', fontSize:'0.7rem', fontWeight:800,
          padding:'3px 12px', borderRadius:999, letterSpacing:'0.5px',
        }}>
          <Star size={10} fill="currentColor"/> TOP PICK
        </span>
        <span style={{
          background:`${catColor}22`, color:catColor,
          border:`1px solid ${catColor}55`,
          padding:'2px 10px', borderRadius:999,
          fontSize:'0.72rem', fontWeight:600,
        }}>
          {stock.category}
        </span>
        <ConvictionBadge level={stock.conviction}/>
      </div>

      {/* Symbol + change */}
      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'0.5rem' }}>
        <span style={{ fontSize:'1.75rem', fontWeight:800, letterSpacing:'0.5px', color:'#f0f4f8' }}>
          {stock.symbol}
        </span>
        <span className={`stock-price ${stock.change >= 0 ? 'positive' : 'negative'}`} style={{ fontSize:'1.2rem' }}>
          {stock.change >= 0 ? <TrendingUp size={18}/> : <TrendingDown size={18}/>}
          {stock.change > 0 ? '+' : ''}{stock.change}%
        </span>
      </div>

      {/* Reason */}
      <div style={{
        fontSize:'0.78rem', color:'#94a3b8', marginBottom:'1rem',
        padding:'6px 10px', background:'rgba(255,255,255,0.03)',
        borderRadius:6, borderLeft:`3px solid ${catColor}`, fontStyle:'italic',
      }}>
        {stock.reason}
      </div>

      {/* Trade Plan — 4 columns */}
      <div style={{
        display:'grid', gridTemplateColumns:'repeat(4,1fr)',
        gap:'0.5rem', fontSize:'0.8rem',
        background:'rgba(0,0,0,0.25)', padding:'0.75rem',
        borderRadius:10, border:'1px solid rgba(255,255,255,0.06)',
      }}>
        {[
          { label:'Entry', value:`₹${stock.entry}`, color:'#60a5fa' },
          { label:'Target', value:`₹${stock.target}`, color:'#34d399' },
          { label:'Stop Loss', value:`₹${stock.sl}`, color:'#f87171' },
          { label:'R:R', value:`1:${rr}`, color:'#f0f4f8' },
        ].map(({ label, value, color }, i) => (
          <div key={i} style={{ textAlign:'center' }}>
            <div style={{ color:'#475569', fontSize:'0.68rem', marginBottom:2 }}>{label}</div>
            <div style={{ color, fontWeight:700, fontSize:'0.95rem' }}>{value}</div>
          </div>
        ))}
      </div>

      <div style={{ marginTop:'0.75rem', fontSize:'0.72rem', color:'#475569', textAlign:'center' }}>
        Click to view full chart →
      </div>
    </div>
  );
};

// ─── Stock Card ──────────────────────────────────────────────────────────────
const StockCard = ({ stock, onClick }) => {
  const catColor = CATEGORY_COLORS[stock.category] || '#94a3b8';
  const isTop = stock.is_top_pick;

  return (
    <div
      className="glass-card clickable-card"
      onClick={() => onClick(stock)}
      style={{
        border: isTop ? `1px solid ${catColor}` : undefined,
        boxShadow: isTop ? `0 0 20px ${catColor}33, 0 8px 24px rgba(0,0,0,0.4)` : undefined,
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Top Pick banner */}
      {isTop && (
        <div style={{
          position: 'absolute', top: 0, right: 0,
          background: `linear-gradient(135deg, ${catColor}cc, ${catColor}88)`,
          color: '#fff', fontSize: '0.7rem', fontWeight: 800,
          padding: '4px 14px', borderBottomLeftRadius: 10,
          display: 'flex', alignItems: 'center', gap: 4,
          letterSpacing: '0.5px',
        }}>
          <Star size={11} fill="currentColor" /> TOP PICK
        </div>
      )}

      {/* Header */}
      <div className="stock-header">
        <div>
          <div className="stock-symbol">{stock.symbol}</div>
          <div style={{ display:'flex', alignItems:'center', gap: 6, marginTop: 4 }}>
            <span style={{
              background: `${catColor}22`, color: catColor,
              border: `1px solid ${catColor}55`,
              padding: '2px 10px', borderRadius: 999,
              fontSize: '0.72rem', fontWeight: 600,
            }}>
              {stock.category}
            </span>
            <ConvictionBadge level={stock.conviction} />
          </div>
        </div>
        <span className={`stock-price ${stock.change >= 0 ? 'positive' : 'negative'}`}>
          {stock.change >= 0 ? <TrendingUp size={18}/> : <TrendingDown size={18}/>}
          {stock.change > 0 ? '+' : ''}{stock.change}%
        </span>
      </div>

      {/* Reason */}
      <div style={{
        fontSize: '0.78rem', color: '#94a3b8', marginBottom: '0.75rem',
        padding: '6px 10px', background: 'rgba(255,255,255,0.03)',
        borderRadius: 6, borderLeft: `3px solid ${catColor}`,
        fontStyle: 'italic',
      }}>
        {stock.reason}
      </div>

      {/* Trade Plan */}
      <div style={{
        display: 'grid', gridTemplateColumns: '1fr 1fr',
        gap: '0.6rem', fontSize: '0.82rem',
        background: 'rgba(0,0,0,0.2)', padding: '0.75rem',
        borderRadius: 8, border: '1px solid var(--border-glass)',
        marginBottom: '0.75rem',
      }}>
        <div style={{ display:'flex', alignItems:'center', gap:6, color:'#60a5fa' }}>
          <TrendingUp size={14}/> Entry: <strong>₹{stock.entry}</strong>
        </div>
        <div style={{ display:'flex', alignItems:'center', gap:6, color:'#34d399' }}>
          <Target size={14}/> Target: <strong>₹{stock.target}</strong>
        </div>
        <div style={{ display:'flex', alignItems:'center', gap:6, color:'#f87171' }}>
          <ShieldAlert size={14}/> SL: <strong>₹{stock.sl}</strong>
        </div>
        <div style={{ display:'flex', alignItems:'center', gap:6, color:'#94a3b8' }}>
          <Clock size={14}/> Hold: <strong>{stock.hold_time}</strong>
        </div>
      </div>

      {/* Mini Chart (non-interactive) */}
      <div style={{ pointerEvents: 'none' }}>
        <LightweightChart data={stock.chart_data} lines={stock.lines} />
      </div>
    </div>
  );
};

// ─── Modal ───────────────────────────────────────────────────────────────────
const StockModal = ({ stock, onClose }) => {
  if (!stock) return null;
  const catColor = CATEGORY_COLORS[stock.category] || '#94a3b8';
  const risk = stock.entry - stock.sl;
  const reward = stock.target - stock.entry;
  const rr = risk > 0 ? (reward / risk).toFixed(1) : 'N/A';

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        {/* Modal Header */}
        <div className="modal-header">
          <div style={{ display:'flex', flexWrap:'wrap', alignItems:'center', gap:'1rem' }}>
            <h2 style={{ fontSize:'2rem', fontWeight:700, margin:0 }}>{stock.symbol}</h2>
            <span style={{
              background: `${catColor}22`, color: catColor,
              border: `1px solid ${catColor}55`,
              padding: '4px 14px', borderRadius: 999,
              fontSize: '0.85rem', fontWeight: 700,
            }}>
              {stock.category}
            </span>
            <ConvictionBadge level={stock.conviction} />
            {stock.is_top_pick && (
              <span style={{
                display:'inline-flex', alignItems:'center', gap:4,
                background: `${catColor}22`, color: catColor,
                border: `1px solid ${catColor}55`,
                padding: '4px 14px', borderRadius: 999,
                fontSize: '0.8rem', fontWeight: 800,
              }}>
                <Star size={13} fill="currentColor"/> Top Pick
              </span>
            )}
            <span className={`stock-price ${stock.change >= 0 ? 'positive' : 'negative'}`} style={{ fontSize:'1.4rem' }}>
              {stock.change >= 0 ? <TrendingUp size={22}/> : <TrendingDown size={22}/>}
              {stock.change > 0 ? '+' : ''}{stock.change}%
            </span>
          </div>
          <button className="modal-close" onClick={onClose}><X size={28}/></button>
        </div>

        <div className="modal-body">
          {/* Reason */}
          <div style={{
            padding:'12px 16px', background:'rgba(255,255,255,0.03)',
            borderRadius:10, borderLeft:`4px solid ${catColor}`,
            fontSize:'0.88rem', color:'#cbd5e1', fontStyle:'italic',
          }}>
            <Award size={14} style={{ display:'inline', marginRight:6, color: catColor }} />
            {stock.reason}
          </div>

          {/* Trade Plan Strip */}
          <div style={{
            display:'grid', gridTemplateColumns:'repeat(5,1fr)',
            gap:'1rem', background:'rgba(0,0,0,0.25)', padding:'1.2rem',
            borderRadius:12, border:'1px solid var(--border-glass)',
          }}>
            {[
              { label:'Entry Price', value:`₹${stock.entry}`, color:'#60a5fa' },
              { label:'Target',      value:`₹${stock.target}`, color:'#34d399' },
              { label:'Stop Loss',   value:`₹${stock.sl}`,     color:'#f87171' },
              { label:'Risk:Reward', value:`1 : ${rr}`,         color:'#f0f4f8' },
              { label:'Hold Time',   value: stock.hold_time,    color:'#f0f4f8' },
            ].map(({ label, value, color }, i) => (
              <div key={i} style={{ textAlign:'center', borderLeft: i > 0 ? '1px solid var(--border-glass)' : 'none' }}>
                <div style={{ color:'#94a3b8', fontSize:'0.78rem', marginBottom:4 }}>{label}</div>
                <div style={{ color, fontSize:'1.4rem', fontWeight:700 }}>{value}</div>
              </div>
            ))}
          </div>

          {/* Big Chart */}
          <LightweightChart data={stock.chart_data} lines={stock.lines} className="modal-chart-container" />
        </div>
      </div>
    </div>
  );
};

// ─── App ─────────────────────────────────────────────────────────────────────
export default function App() {
  const [results, setResults]         = useState([]);
  const [loading, setLoading]         = useState(false);
  const [error, setError]             = useState(null);
  const [lastScan, setLastScan]       = useState(null);
  const [selectedStock, setSelectedStock] = useState(null);
  const [activeCategory, setActiveCategory] = useState('All');

  const handleScan = async () => {
    setLoading(true); setError(null);
    try {
      const res = await axios.get('http://localhost:8080/api/scan');
      setResults(res.data);
      setLastScan(new Date().toLocaleTimeString());
      setActiveCategory('All');
    } catch (err) {
      setError('Failed to fetch data. Ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  // Derive categories from results
  const categories = ['All', ...Object.keys(
    results.reduce((acc, s) => { acc[s.category] = true; return acc; }, {})
  )];

  const filtered = activeCategory === 'All'
    ? results
    : results.filter(s => s.category === activeCategory);

  const topPicks = results.filter(s => s.is_top_pick);

  return (
    <div className="app-container">
      <header className="header">
        <h1><Activity color="#06b6d4" size={36}/>Nifty 250 Scanner</h1>
        {lastScan && <span style={{ color:'#475569', fontSize:'0.85rem' }}>Last scan: {lastScan}</span>}
      </header>

      <main className="dashboard">
        {/* ── Sidebar ── */}
        <aside className="controls-panel">
          <div className="glass-card">
            <h2 style={{ marginBottom:'1.25rem', display:'flex', alignItems:'center', gap:8 }}>
              <TrendingUp size={18} color="#3b82f6"/> Control Center
            </h2>
            <button
              className={`btn ${!loading ? 'btn-pulse' : ''}`}
              onClick={handleScan} disabled={loading}
              style={{ width:'100%', justifyContent:'center' }}
            >
              {loading
                ? <><RefreshCw size={18} style={{ animation:'spin 1s linear infinite' }}/> Scanning…</>
                : <><Play size={18} fill="currentColor"/> Run Market Scan</>}
            </button>
          </div>

          <div className="stat-box">
            <div className="stat-value">{results.length}</div>
            <div className="stat-label">Breakouts Found</div>
          </div>
          <div className="stat-box">
            <div className="stat-value" style={{ color:'#f59e0b', textShadow:'0 0 10px rgba(245,158,11,0.5)' }}>
              {topPicks.length}
            </div>
            <div className="stat-label">Top Picks</div>
          </div>

          <div className="glass-card">
            <h3 style={{ fontSize:'0.9rem', marginBottom:'0.75rem', color:'var(--text-secondary)' }}>
              Patterns Scanned
            </h3>
            <ul style={{ listStyle:'none', display:'flex', flexDirection:'column', gap:6, fontSize:'0.82rem' }}>
              {Object.entries(CATEGORY_COLORS).map(([name, color]) => (
                <li key={name} style={{ display:'flex', alignItems:'center', gap:8 }}>
                  <span style={{ width:8, height:8, borderRadius:'50%', background:color, flexShrink:0 }}/>
                  {name}
                </li>
              ))}
            </ul>
          </div>
        </aside>

        {/* ── Main Content ── */}
        <section>
          {error && (
            <div className="glass-card" style={{ borderColor:'var(--accent-red)', marginBottom:'1.5rem', display:'flex', alignItems:'center', gap:'1rem', color:'var(--accent-red)' }}>
              <AlertCircle size={24}/><p>{error}</p>
            </div>
          )}

          {loading ? (
            <div className="loading-container glass-card">
              <div className="spinner"/>
              <div className="loading-text">Scanning Nifty 250…</div>
              <p style={{ color:'#475569', fontSize:'0.85rem', marginTop:'0.5rem' }}>This may take 30–60 seconds · Using 2 years of data</p>
            </div>
          ) : results.length > 0 ? (
            <>
              {/* ── Top Picks Hero Section ── */}
              {topPicks.length > 0 && (
                <div style={{ marginBottom: '2.5rem' }}>
                  <div style={{ display:'flex', alignItems:'center', gap: 10, marginBottom: '1rem' }}>
                    <Star size={20} color="#f59e0b" fill="#f59e0b"/>
                    <h2 style={{ fontSize:'1.2rem', fontWeight:700, background:'linear-gradient(to right,#f59e0b,#fbbf24)', WebkitBackgroundClip:'text', WebkitTextFillColor:'transparent' }}>
                      Top Picks · Best Setup Per Category
                    </h2>
                    <span style={{ marginLeft:'auto', fontSize:'0.78rem', color:'#475569' }}>
                      Click a card to expand
                    </span>
                  </div>
                  <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fill, minmax(340px,1fr))', gap:'1.25rem' }}>
                    {topPicks.map((stock, idx) => (
                      <TopPickHeroCard key={idx} stock={stock} onClick={setSelectedStock}/>
                    ))}
                  </div>
                </div>
              )}

              {/* Divider */}
              <div style={{ display:'flex', alignItems:'center', gap:12, marginBottom:'1.5rem' }}>
                <div style={{ flex:1, height:1, background:'var(--border-glass)' }}/>
                <span style={{ color:'#475569', fontSize:'0.82rem', whiteSpace:'nowrap' }}>All Breakout Setups</span>
                <div style={{ flex:1, height:1, background:'var(--border-glass)' }}/>
              </div>

              {/* Category Filter Tabs */}
              <div style={{ display:'flex', flexWrap:'wrap', gap:'0.5rem', marginBottom:'1.5rem' }}>
                {categories.map(cat => {
                  const color = cat === 'All' ? '#94a3b8' : (CATEGORY_COLORS[cat] || '#94a3b8');
                  const isActive = activeCategory === cat;
                  return (
                    <button key={cat} onClick={() => setActiveCategory(cat)} style={{
                      padding:'6px 16px', borderRadius:999, fontSize:'0.8rem', fontWeight:600,
                      cursor:'pointer', transition:'all 0.2s',
                      background: isActive ? `${color}22` : 'transparent',
                      color: isActive ? color : '#94a3b8',
                      border: `1px solid ${isActive ? color : 'rgba(255,255,255,0.08)'}`,
                      boxShadow: isActive ? `0 0 10px ${color}33` : 'none',
                    }}>
                      {cat}
                      {cat !== 'All' && (
                        <span style={{ marginLeft:6, opacity:0.7 }}>
                          ({results.filter(s => s.category === cat).length})
                        </span>
                      )}
                    </button>
                  );
                })}
              </div>

              {/* Main Results Grid — non-top-picks only (or filtered) */}
              <div className="results-grid">
                {filtered.filter(s => !s.is_top_pick).map((stock, idx) => (
                  <StockCard key={idx} stock={stock} onClick={setSelectedStock}/>
                ))}
              </div>
            </>
          ) : (
            <div className="empty-state">
              <Activity size={48} className="empty-icon"/>
              <h2>Ready to Scan</h2>
              <p style={{ marginTop:'0.5rem' }}>
                Click <strong>Run Market Scan</strong> to identify high-conviction breakout setups across Nifty 250.
                <br/><span style={{ opacity:0.6, fontSize:'0.85rem' }}>Filters: Close &gt; 50 EMA · Bullish Supertrend (10,2) · 2 Years Data</span>
              </p>
            </div>
          )}
        </section>
      </main>

      <StockModal stock={selectedStock} onClose={() => setSelectedStock(null)}/>
    </div>
  );
}
