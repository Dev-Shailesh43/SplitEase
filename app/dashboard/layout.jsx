'use client';

import Link from 'next/link';

export default function DashboardLayout({ children }) {
  return (
    <div style={{ display: 'flex', height: '100vh', width: '100vw', overflow: 'hidden' }}>
      
      {/* 1. Left Rail (Pods Switcher) */}
      <nav style={{ width: '72px', backgroundColor: 'rgba(15, 23, 42, 0.95)', borderRight: '1px solid var(--glass-border)', display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '1rem 0', gap: '1rem', zIndex: 10 }}>
        
        {/* Home / Direct Friends */}
        <Link href="/dashboard" title="Home" style={{ width: '48px', height: '48px', borderRadius: '14px', background: 'var(--accent-gradient)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', transition: 'all 0.2s' }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
        </Link>
        
        <div style={{ width: '32px', height: '2px', backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: '2px' }} />

        {/* Mock Pods */}
        <button style={{ width: '48px', height: '48px', borderRadius: '24px', backgroundColor: '#334155', border: 'none', color: 'white', fontSize: '1.2rem', fontWeight: 'bold', cursor: 'pointer', transition: 'all 0.2s' }}>
          H1
        </button>
        <button style={{ width: '48px', height: '48px', borderRadius: '24px', backgroundColor: '#334155', border: 'none', color: 'white', fontSize: '1.2rem', fontWeight: 'bold', cursor: 'pointer', transition: 'all 0.2s' }}>
          HT
        </button>

        {/* Add Pod */}
        <button style={{ width: '48px', height: '48px', borderRadius: '24px', backgroundColor: 'rgba(16, 185, 129, 0.1)', border: '1px dashed var(--success)', color: 'var(--success)', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', marginTop: 'auto', transition: 'all 0.2s' }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        </button>

      </nav>

      {/* 2. Middle Sidebar (Channels) */}
      <aside style={{ width: '260px', backgroundColor: 'rgba(30, 41, 59, 0.8)', backdropFilter: 'blur(10px)', borderRight: '1px solid var(--glass-border)', display: 'flex', flexDirection: 'column' }}>
        
        {/* Header */}
        <header style={{ padding: '1.25rem 1rem', borderBottom: '1px solid var(--glass-border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }}>
          <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-primary)' }}>Hackathon Team</h2>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="6 9 12 15 18 9"/></svg>
        </header>

        {/* Channels */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '1rem 0.5rem' }}>
          
          <div style={{ marginBottom: '1.5rem' }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-secondary)', paddingLeft: '0.75rem', letterSpacing: '0.05em' }}>FINANCIAL CHANNELS</span>
            <div style={{ marginTop: '0.5rem', display: 'flex', flexDirection: 'column', gap: '2px' }}>
              
              <Link href="/dashboard" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.5rem 0.75rem', borderRadius: '8px', backgroundColor: 'rgba(255,255,255,0.05)', color: 'var(--text-primary)' }}>
                <span style={{ color: 'var(--text-secondary)' }}>#</span> overview
              </Link>
              <Link href="/dashboard/expenses" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.5rem 0.75rem', borderRadius: '8px', color: 'var(--text-secondary)' }}>
                <span style={{ color: 'var(--text-secondary)' }}>#</span> expenses
              </Link>
              <Link href="/dashboard/settle" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.5rem 0.75rem', borderRadius: '8px', color: 'var(--text-secondary)' }}>
                <span style={{ color: 'var(--text-secondary)' }}>#</span> settle-up
                <span style={{ marginLeft: 'auto', backgroundColor: 'var(--danger)', color: 'white', fontSize: '0.7rem', padding: '2px 6px', borderRadius: '10px', fontWeight: 'bold' }}>1</span>
              </Link>
              <Link href="/dashboard/analytics" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.5rem 0.75rem', borderRadius: '8px', color: 'var(--text-secondary)' }}>
                <span style={{ color: 'var(--text-secondary)' }}>#</span> analytics
              </Link>

            </div>
          </div>

          <div>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-secondary)', paddingLeft: '0.75rem', letterSpacing: '0.05em' }}>MANAGEMENT</span>
            <div style={{ marginTop: '0.5rem', display: 'flex', flexDirection: 'column', gap: '2px' }}>
              <Link href="/dashboard/members" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.5rem 0.75rem', borderRadius: '8px', color: 'var(--text-secondary)' }}>
                <span style={{ color: 'var(--text-secondary)' }}>#</span> members
              </Link>
            </div>
          </div>

        </div>

        {/* User Footer */}
        <footer style={{ padding: '1rem', borderTop: '1px solid var(--glass-border)', backgroundColor: 'rgba(15, 23, 42, 0.4)', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{ width: '36px', height: '36px', borderRadius: '18px', backgroundColor: 'var(--accent-primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>A</div>
          <div style={{ flex: 1, overflow: 'hidden' }}>
            <div style={{ fontSize: '0.9rem', fontWeight: 600, whiteSpace: 'nowrap', textOverflow: 'ellipsis' }}>Aman Sharma</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>#CAMP-7492</div>
          </div>
          <button style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer' }}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
          </button>
        </footer>

      </aside>

      {/* 3. Main Viewport */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', backgroundColor: 'var(--bg-primary)', position: 'relative' }}>
        
        {/* Top Channel Bar */}
        <header style={{ height: '56px', borderBottom: '1px solid var(--glass-border)', display: 'flex', alignItems: 'center', padding: '0 1.5rem', gap: '1rem', backgroundColor: 'rgba(15, 23, 42, 0.8)', backdropFilter: 'blur(8px)' }}>
          <div style={{ fontSize: '1.2rem', color: 'var(--text-secondary)' }}>#</div>
          <div style={{ fontWeight: 700, color: 'var(--text-primary)' }}>overview</div>
          <div style={{ width: '1px', height: '24px', backgroundColor: 'var(--glass-border)', margin: '0 0.5rem' }}></div>
          <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', flex: 1 }}>Hackathon Team — Pod overview & balances</div>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div className="glass-panel" style={{ padding: '4px 12px', borderRadius: '16px', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem', color: 'var(--success)' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '4px', backgroundColor: 'var(--success)' }}></div>
              Cloud Live
            </div>
            <button className="btn btn-primary" style={{ padding: '0.4rem 1rem', fontSize: '0.85rem' }}>
              + Expense
            </button>
          </div>
        </header>

        {/* Content Area */}
        <main style={{ flex: 1, overflowY: 'auto', padding: '2rem' }}>
          {children}
        </main>
      </div>

    </div>
  );
}
