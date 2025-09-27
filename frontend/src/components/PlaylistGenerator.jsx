import React from 'react';
import '../styles/PlaylistGenerator.css';

const PlaylistGenerator = () => {
    return (
        <div className="playlist-generator-container">
            <h1>Enter your mood</h1>
            <textarea
                className='std-box'

                placeholder='how are you feeling today'
                style={{ resize: 'none' }}
            />
            <button className='std-box'><h2>Generate</h2></button>
        </div>
    );
};

export default PlaylistGenerator;