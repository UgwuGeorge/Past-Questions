import React from 'react';
import './styles/global.css';

function App() {
  const exams = [
    { id: 1, name: "JAMB", category: "Admission", icon: "🎓" },
    { id: 2, name: "ICAN", category: "Professional", icon: "💼" },
    { id: 3, name: "IELTS", category: "Language", icon: "🌍" },
    { id: 4, name: "PTDF Scholarship", category: "Scholarship", icon: "⭐" },
  ];

  return (
    <div className="app-container">
      <nav style={{ padding: '1.5rem', borderBottom: '1px solid var(--glass-border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ margin: 0 }}>AI Exam Prep</h2>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button className="btn btn-primary">Login</button>
        </div>
      </nav>

      <main style={{ padding: '2rem' }}>
        <header style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <h1 style={{ fontSize: '3rem' }}>Master Your Future</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.2rem' }}>AI-powered preparation for Nigerian & International Exams</p>
        </header>

        <div className="dashboard-grid">
          {exams.map(exam => (
            <div key={exam.id} className="glass-card">
              <span style={{ fontSize: '2rem' }}>{exam.icon}</span>
              <h3 style={{ marginTop: '1rem' }}>{exam.name}</h3>
              <p style={{ color: 'var(--text-muted)' }}>{exam.category}</p>
              <button className="btn btn-primary" style={{ marginTop: '1.5rem', width: '100%', background: 'rgba(99, 102, 241, 0.2)', border: '1px solid var(--primary)' }}>
                Start Practice
              </button>
            </div>
          ))}
        </div>

        <section style={{ marginTop: '4rem', padding: '2rem' }} className="glass-card">
          <h2>AI Intelligence Hub</h2>
          <div className="dashboard-grid" style={{ padding: 0 }}>
            <div>
              <h3>Essay Grading</h3>
              <p style={{ color: 'var(--text-muted)' }}>Upload your SOP or IELTS essay for instant AI feedback.</p>
              <button className="btn btn-primary" style={{ marginTop: '1rem' }}>Grade My Essay</button>
            </div>
            <div>
              <h3>Interview Simulation</h3>
              <p style={{ color: 'var(--text-muted)' }}>Interactive AI-led interview prep for scholarships.</p>
              <button className="btn btn-primary" style={{ marginTop: '1rem' }}>Start Mock Interview</button>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
