import { BookText, Bot, Briefcase, Menu, MessageSquareText, Shield, UserCircle2 } from 'lucide-react';
import './App.css';

const quickActions = [
  { title: 'Practice Exams', icon: BookText, tone: 'orange' },
  { title: 'Essay Grading', icon: MessageSquareText, tone: 'blue' },
  { title: 'Interview Prep', icon: Bot, tone: 'teal' },
];

const recommendations = [
  { title: 'JAMB UTME', text: 'Take mock CBT exam', badge: 'JAMB' },
  { title: 'IELTS', text: 'Improve your writing skills', badge: 'IELTS' },
  { title: 'Commonwealth Scholarship', text: 'Practice scholarship interview', badge: 'CWS' },
];

const supported = [
  { title: 'WAEC', kind: 'Academic Exam', icon: Shield },
  { title: 'JAMB', kind: 'Academic Exam', icon: Briefcase },
  { title: 'ICAN', kind: 'Professional Exam', icon: UserCircle2 },
];

function App() {
  return (
    <div className="page-shell">
      <main className="dashboard">
        <header className="topbar">
          <div className="brand">
            <span className="brand-icon">
              <Briefcase size={18} />
            </span>
            <span>AI-Powered Exam & Scholarship Preparation Platform</span>
          </div>
          <nav className="menu">
            <a href="#">Home</a>
            <a href="#">Exams</a>
            <a href="#">Scholarships</a>
            <a href="#">Profile</a>
          </nav>
          <button className="menu-btn" aria-label="Open menu">
            <Menu size={18} />
          </button>
        </header>

        <section className="content">
          <h1>Welcome Back, Daniel!</h1>

          <div className="quick-actions">
            {quickActions.map((item) => {
              const Icon = item.icon;
              return (
                <button key={item.title} className={`quick-card ${item.tone}`}>
                  <Icon size={24} />
                  <span>{item.title}</span>
                </button>
              );
            })}
          </div>

          <section className="panel">
            <h2>Recommended For You</h2>
            <div className="cards-grid">
              {recommendations.map((item) => (
                <article key={item.title} className="info-card">
                  <span className="pill">{item.badge}</span>
                  <h3>{item.title}</h3>
                  <p>{item.text}</p>
                  <button>Start</button>
                </article>
              ))}
            </div>
          </section>

          <section className="panel">
            <h2>Supported Exams & Scholarships</h2>
            <div className="cards-grid compact">
              {supported.map((item) => {
                const Icon = item.icon;
                return (
                  <article key={item.title} className="mini-card">
                    <Icon size={20} />
                    <div>
                      <h3>{item.title}</h3>
                      <p>{item.kind}</p>
                    </div>
                  </article>
                );
              })}
            </div>
          </section>
        </section>
      </main>
    </div>
  );
}

export default App;
