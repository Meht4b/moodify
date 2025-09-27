import React from 'react';
import '../styles/Playlist.css'

const Playlist = () => {
    return (
        <> 
            <div className='playlist-container'>

                <iframe
                    style={{ borderRadius: '12px' }}
                    src="https://open.spotify.com/embed/playlist/37i9dQZF1E8MgmCOsdOYXb?utm_source=generator"
                    width="100%"
                    height="352"
                    frameBorder="0"
                    allowFullScreen
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                    loading="lazy"
                ></iframe>
            </div>
        </>
    );
};

export default Playlist;