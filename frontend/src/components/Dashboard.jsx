import { useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import PlaybackControls from './PlaybackControls.jsx';

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

  return <div>
      <h1>Spotify Dashboard</h1>
      <PlaybackControls accessToken={localStorage.getItem("access_token")} />
    </div>;
}

export default Dashboard;
