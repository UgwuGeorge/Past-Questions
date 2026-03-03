import { Briefcase, ChevronRight, MessageSquare, Play } from 'lucide-react';
import './App.css';

const quickActions = [
  { title: 'Practice Exams', icon: '📝', tone: 'orange' },
  { title: 'Essay Grading', icon: '💬', tone: 'blue' },
  { title: 'Interview Prep', icon: '👤', tone: 'teal' },
];

const recommendations = [
  { 
    title: 'JAMB UTME', 
    text: 'Take mock CBT exam', 
    badge: 'JAMB', 
    logo: '/assets/jamb_logo.png' 
  },
  { 
    title: 'IELTS', 
    text: 'Improve your writing skills', 
    badge: 'IELTS', 
    logo: '/assets/ielts_logo.png' 
  },
  { 
    title: 'Commonwealth Scholarship', 
    text: 'Practice scholarship interview', 
    badge: 'CWS', 
    logo: '/assets/cws_logo.png' 
  },
];

const supported = [
  { title: 'WAEC', kind: 'Academic Exam', logo: '/assets/waec_logo.png' },
  { title: 'JAMB', kind: 'Academic Exam', logo: '/assets/jamb_logo.png' },
  { title: 'ICAN', kind: 'Professional Exam', logo: '/assets/cws_logo.png' },
];

function App() {
  return (
    <div className="page-shell">
      <main className="dashboard">
        <header className="topbar">
          <div className="brand">
            <div className="brand-icon">
              <Briefcase size={20} />
            </div>
            <span>AI-Powered Exam & Scholarship Preparation Platform</span>
          </div>
          
          <nav className="nav-links">
            <a href="#">Home</a>
            <a href="#">Exams</a>
            <a href="#">Scholarships</a>
            <a href="#">Profile</a>
          </nav>

          <div className="user-profile">
            <img src="/assets/user_avatar.png" alt="User" className="avatar" />
            <div className="menu-icon">
              <div style={{width: 20, height: 2, background: 'white', marginBottom: 4}}></div>
              <div style={{width: 20, height: 2, background: 'white', marginBottom: 4}}></div>
              <div style={{width: 15, height: 2, background: 'white'}}></div>
            </div>
          </div>
        </header>

        <section className="content">
          <h1>Welcome Back, Daniel!</h1>

          <div className="quick-actions">
            {quickActions.map((item) => (
              <button key={item.title} className={`quick-card ${item.tone}`}>
                <span className="card-emoji">{item.icon}</span>
                <span>{item.title}</span>
              </button>
            ))}
          </div>

          <section className="section-panel">
            <h2>Recommended For You</h2>
            <div className="cards-grid">
              {recommendations.map((item) => (
                <article key={item.title} className="info-card">
                  <div className="card-header">
                    <img src={item.logo} alt={item.badge} className="card-logo" />
                    <div className="card-title-group">
                      <span className="badge">{item.badge}</span>
                      <h3>{item.title}</h3>
                    </div>
                  </div>
                  <p>{item.text}</p>
                  <button className="btn-start">
                    Start <ChevronRight size={16} />
                  </button>
                </article>
              ))}
            </div>
          </section>

          <section className="section-panel">
            <h2>Supported Exams & Scholarships</h2>
            <div className="cards-grid">
              {supported.map((item) => (
                <article key={item.title} className="mini-card">
                  <img src={item.logo} alt={item.title} className="mini-logo" />
                  <div className="mini-info">
                    <h3>{item.title}</h3>
                    <p>{item.kind}</p>
                  </div>
                </article>
              ))}
            </div>
          </section>
        </section>

        <div className="ask-ai-fab">
          <div className="bot-icon-wrapper">
             <MessageSquare size={20} />
             <div className="bot-badge">1</div>
          </div>
          <span>Ask AI</span>
        </div>
      </main>
    </div>
  );
}

export default App;

