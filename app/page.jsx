import Link from 'next/link';

export default function Home() {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem' }}>
      <div className="glass-panel animate-fade-in-up" style={{ maxWidth: '900px', width: '100%', padding: '4rem 3rem', textAlign: 'center' }}>
        
        <div style={{ marginBottom: '3rem' }}>
          <div style={{ display: 'inline-block', padding: '0.5rem 1rem', background: 'rgba(99, 102, 241, 0.1)', border: '1px solid rgba(99, 102, 241, 0.2)', borderRadius: '20px', color: 'var(--accent-primary)', fontSize: '0.9rem', fontWeight: 600, marginBottom: '1.5rem' }}>
            ✨ Introducing Version 2.0
          </div>
          <h1 style={{ fontSize: '4.5rem', fontWeight: 800, marginBottom: '1.5rem', lineHeight: 1.1 }}>
            Welcome to <span className="text-gradient">SplitEase</span>
          </h1>
          <p style={{ fontSize: '1.25rem', color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto', lineHeight: 1.6 }}>
            The smartest way to split expenses, track campus debts, and settle up instantly with zero friction.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '1.5rem', justifyContent: 'center', marginTop: '2.5rem' }}>
          <Link href="/dashboard" className="btn btn-primary" style={{ padding: '1.2rem 2.5rem', fontSize: '1.1rem' }}>
            Open Dashboard
          </Link>
          <Link href="/auth/login" className="btn btn-secondary" style={{ padding: '1.2rem 2.5rem', fontSize: '1.1rem' }}>
            Sign In
          </Link>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '2rem', marginTop: '5rem', textAlign: 'left' }}>
          <div className="glass-panel" style={{ padding: '2rem', background: 'rgba(255,255,255,0.02)' }}>
            <h3 style={{ color: 'var(--accent-primary)', marginBottom: '0.75rem', fontSize: '1.2rem' }}>⚡ Smart Settlement</h3>
            <p style={{ fontSize: '0.95rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>Our graph-minimized algorithm reduces N*(N-1) complex transfers into just a few simple payments.</p>
          </div>
          <div className="glass-panel" style={{ padding: '2rem', background: 'rgba(255,255,255,0.02)' }}>
            <h3 style={{ color: 'var(--success)', marginBottom: '0.75rem', fontSize: '1.2rem' }}>🏦 1-Tap UPI</h3>
            <p style={{ fontSize: '0.95rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>Pre-filled deep links for instant payments via Google Pay, PhonePe, or Paytm.</p>
          </div>
          <div className="glass-panel" style={{ padding: '2rem', background: 'rgba(255,255,255,0.02)' }}>
            <h3 style={{ color: 'var(--warning)', marginBottom: '0.75rem', fontSize: '1.2rem' }}>🔒 Cloud Sync API</h3>
            <p style={{ fontSize: '0.95rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>Full-stack Next.js API architecture ensuring real-time synchronization across devices.</p>
          </div>
        </div>

      </div>
    </div>
  );
}
