import React, { createContext, useContext, useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); 
  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

const Navbar = () => {
  const { user, setUser } = useContext(AuthContext);
  return (
    <nav style={{ padding: '15px', background: '#2c3e50', color: 'white', display: 'flex', gap: '20px', alignItems: 'center' }}>
      <Link to="/dashboard" style={{ color: 'white', textDecoration: 'none' }}>🏠 Dashboard</Link>
      <Link to="/profile" style={{ color: 'white', textDecoration: 'none' }}>👤 Profile</Link>
      <div style={{ marginLeft: 'auto' }}>
        <span>Welcome, <b>{user?.name}</b>! </span>
        <button onClick={() => setUser(null)} style={{ marginLeft: '10px', cursor: 'pointer' }}>Logout</button>
      </div>
    </nav>
  );
};

const LoginPage = () => {
  const { setUser } = useContext(AuthContext);
  const [name, setName] = useState("");
  const navigate = useNavigate();

  const handleLogin = () => {
    if (name.trim()) {
      setUser({ 
        name, 
        role: "Administrator", 
        loginTime: new Date().toLocaleString() 
      });
      navigate('/dashboard');
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', marginTop: '100px' }}>
      <div style={{ padding: '30px', border: '1px solid #ccc', borderRadius: '10px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
        <h2>SmartHome Login</h2>
        <input 
          type="text"
          placeholder="Enter your name" 
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{ padding: '10px', width: '250px', marginBottom: '10px', display: 'block' }}
        />
        <button onClick={handleLogin} style={{ padding: '10px 20px', width: '100%', cursor: 'pointer', background: '#3498db', color: 'white', border: 'none', borderRadius: '5px' }}>
          Login
        </button>
      </div>
    </div>
  );
};

const DashboardPage = () => {
  const [homes, setHomes] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/homes')
      .then(res => res.json())
      .then(data => setHomes(data))
      .catch(err => console.error("Error"));
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h2>Your Smart Objects</h2>
      {homes.length === 0 && <p>No data found.</p>}
      
      {homes.map(home => (
        <div key={home.id} style={{ border: '2px solid #3498db', borderRadius: '10px', margin: '20px 0', padding: '20px', background: '#f9f9f9' }}>
          <h3 style={{ color: '#2980b9', marginTop: 0 }}>📍 Address: {home.address}</h3>
          <p>Owner: <b>{home.owner}</b></p>
          
          {home.rooms.map(room => (
            <div key={room.id} style={{ marginLeft: '30px', marginTop: '15px', padding: '10px', borderLeft: '4px solid #bdc3c7', background: '#fff' }}>
              <h4 style={{ margin: '0 0 10px 0' }}>🚪 Room: {room.name}</h4>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                {room.devices.map(device => (
                  <div key={device.id} style={{ padding: '10px', border: '1px solid #ddd', borderRadius: '5px', minWidth: '150px' }}>
                    <b>📟 {device.name}</b><br/>
                    <small>Type: {device.type}</small><br/>
                    <span style={{ color: device.status === 'online' ? '#27ae60' : '#e74c3c', fontWeight: 'bold' }}>
                      ● {device.status}
                    </span>
                  </div>
                ))}
                {room.devices.length === 0 && <span style={{ color: '#95a5a6' }}>No devices</span>}
              </div>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

const ProfilePage = () => {
  const { user } = useContext(AuthContext);
  return (
    <div style={{ padding: '20px' }}>
      <h2>User Profile</h2>
      <div style={{ background: '#ecf0f1', padding: '20px', borderRadius: '10px' }}>
        <p><b>Name:</b> {user?.name}</p>
        <p><b>Role:</b> {user?.role}</p>
        <p><b>Last Login:</b> {user?.loginTime}</p>
      </div>
    </div>
  );
};

const ProtectedRoute = ({ children }) => {
  const { user } = useContext(AuthContext);
  return user ? children : <Navigate to="/login" />;
};

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/dashboard" element={<ProtectedRoute><Navbar /><DashboardPage /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><Navbar /><ProfilePage /></ProtectedRoute>} />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}