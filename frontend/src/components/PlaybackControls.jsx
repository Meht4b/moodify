import React, { useEffect, useState } from "react";
import "../styles/PlaybackControls.css";
import PlayIcon from "../assets/play.png";
import PauseIcon from "../assets/stop.png";
import PrevIcon from "../assets/prev.png";
import NextIcon from "../assets/next.png";


function PlaybackToggle({ accessToken }) {
  const [isPlaying, setIsPlaying] = useState(false);

  const nextTrack = async () => {
  const res = await fetch('https://api.spotify.com/v1/me/player/next', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (res.status === 204) {
    console.log("Skipped to next track");
  } else {
    const errorText = await res.text();
    console.error("Failed to skip to next track:", errorText);
  }
};

const previousTrack = async () => {
  const res = await fetch('https://api.spotify.com/v1/me/player/previous', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (res.status === 204) {
    console.log("Went back to previous track");
  } else {
    const errorText = await res.text();
    console.error("Failed to go to previous track:", errorText);
  }
};


  const headers = {
    Authorization: `Bearer ${accessToken}`,
    "Content-Type": "application/json",
  };

  // Check current playback state
  const checkPlayback = async () => {
    const res = await fetch("https://api.spotify.com/v1/me/player", {
      headers,
    });

    if (res.status === 200) {
      const data = await res.json();
      setIsPlaying(data.is_playing);
    } else {
      console.error("Failed to get playback state", await res.json());
    }
  };

  // Toggle play/pause depending on current state
  const togglePlayback = async () => {
    const endpoint = isPlaying
        ? "https://api.spotify.com/v1/me/player/pause"
        : "https://api.spotify.com/v1/me/player/play";

    const method = "PUT";

    const res = await fetch(endpoint, {
        method,
        headers,
    });

    if (res.status === 204) {
        setIsPlaying(!isPlaying);
    } else {
        // Try to parse JSON if possible, otherwise show text
        let errorText;
        try {
        errorText = await res.text(); // get raw text
        const errorJson = JSON.parse(errorText);
        console.error("Failed to toggle playback:", errorJson);
        } catch {
        console.error("Failed to toggle playback:", errorText);
        }
    }
    checkPlayback(); // Refresh state after toggling
    };


  // Check playback state on mount
  useEffect(() => {
    if (accessToken) {
      checkPlayback();
    }
  }, [accessToken]);

return (
    <>
    <div className="std-box playback-controls-container">
        <button className="playback-skip-btn" onClick={previousTrack}>
            <img src={PrevIcon} alt="" />
        </button>
        <button onClick={togglePlayback} className="playback-toggle-btn">
            <img
                src={PlayIcon}
                alt="Play"
                className={`playback-icon play-icon ${isPlaying ? "fade-out" : "fade-in"}`}
            />
            <img
                src={PauseIcon}
                alt="Pause"
                className={`playback-icon pause-icon ${isPlaying ? "fade-in" : "fade-out"}`
              }
            />
        </button>
        <button className="playback-skip-btn" onClick={nextTrack}>
            <img src={NextIcon} alt="" />
        </button>
    </div>
    </>
);
}

export default PlaybackToggle;
