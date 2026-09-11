export default function DashboardPage() {
  return (
    <div className="animate-fade-in-up" style={{ maxWidth: '1000px', margin: '0 auto' }}>
      
      {/* Overview Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem', marginBottom: '3rem' }}>
        
        <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Total Group Spending</span>
          <span style={{ fontSize: '2.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>₹4,250</span>
          <span style={{ fontSize: '0.85rem', color: 'var(--success)' }}>↑ 12% from last week</span>
        </div>

        <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Your Balance</span>
          <span style={{ fontSize: '2.5rem', fontWeight: 800, color: 'var(--success)' }}>+₹650</span>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>You are owed money</span>
        </div>

      </div>

      {/* Action Area */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
        
        {/* Recent Expenses List */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Recent Expenses</h3>
            <button className="btn btn-secondary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}>View All</button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            
            {/* Expense Item */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', padding: '1rem', backgroundColor: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.05)' }}>
              <div style={{ width: '48px', height: '48px', borderRadius: '12px', backgroundColor: 'rgba(99, 102, 241, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.5rem' }}>
                🍕
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 600, fontSize: '1.05rem' }}>Hackathon Dinner</div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Paid by Aman • Today</div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontWeight: 700, fontSize: '1.1rem' }}>₹1,200</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>You owe ₹300</div>
              </div>
            </div>

            {/* Expense Item */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', padding: '1rem', backgroundColor: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.05)' }}>
              <div style={{ width: '48px', height: '48px', borderRadius: '12px', backgroundColor: 'rgba(16, 185, 129, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.5rem' }}>
                🚕
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 600, fontSize: '1.05rem' }}>Uber to Campus</div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Paid by You • Yesterday</div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontWeight: 700, fontSize: '1.1rem' }}>₹450</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--success)' }}>You lent ₹225</div>
              </div>
            </div>

          </div>
        </div>

        {/* Quick Settle Panel */}
        <div className="glass-panel" style={{ padding: '1.5rem', background: 'var(--accent-gradient)', color: 'white', border: 'none' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '1rem' }}>Action Required</h3>
          <p style={{ fontSize: '0.9rem', marginBottom: '1.5rem', opacity: 0.9 }}>
            Debt simplification has reduced 4 transfers down to 1 direct payment.
          </p>
          
          <div style={{ backgroundColor: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '12px', marginBottom: '1.5rem' }}>
            <div style={{ fontSize: '0.85rem', opacity: 0.8, marginBottom: '0.25rem' }}>You owe</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 800 }}>Priya Patel</div>
            <div style={{ fontSize: '1.25rem', fontWeight: 600, marginTop: '0.5rem' }}>₹300</div>
          </div>

          <button className="btn" style={{ width: '100%', backgroundColor: 'white', color: 'var(--accent-primary)', fontWeight: 800, padding: '1rem' }}>
            Pay via UPI Now
          </button>
        </div>

      </div>

    </div>
  );
}
