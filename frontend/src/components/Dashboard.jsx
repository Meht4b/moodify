import { useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import '../styles/Dashboard.css'
import PlaybackControls from './PlaybackControls.jsx';
import Header from './Header.jsx'

function Dashboard() {
  const [searchParams] = useSearchParams();

  useEffect(() => {
    const accessToken = searchParams.get("access_token");
    const refreshToken = searchParams.get("refresh_token");

    if (accessToken) {
      localStorage.setItem("access_token", accessToken);
      localStorage.setItem("refresh_token", refreshToken);
    }

    // Now you're authenticated!
    console.log("Access token:", accessToken);
  }, []);

  return (
    <div className='dashboard-container'>
        <Header/>
        <PlaybackControls accessToken={localStorage.getItem("access_token")} />
    </div>

  )
}

export default Dashboard;
