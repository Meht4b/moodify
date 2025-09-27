import React, { useEffect, useState } from "react";

function PlaybackToggle({ accessToken }) {
  const [isPlaying, setIsPlaying] = useState(false);

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
    <button onClick={togglePlayback}>
      {isPlaying ? "⏸️ Pause" : "▶️ Play"}
    </button>
  );
}

export default PlaybackToggle;
