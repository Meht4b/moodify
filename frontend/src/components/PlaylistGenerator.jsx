import React, { useState } from 'react';
import '../styles/PlaylistGenerator.css';

const PlaylistGenerator = () => {
    const [value,setValue] = useState('')
   const handleSubmit = async (e) => {
        e.preventDefault();
        const val = value
        const url = "http://127.0.0.1:5000/create_playlist"



        const options = {
            method:"POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                'access_token':localStorage.getItem("access_token"),
                'refresh_token':localStorage.getItem("refresh_token"),
                'prompt':val
            }),
        };




        const response = await fetch(url, options);
        const data = await response.json();
        if (response.ok) {
            console.log(data);
        } else {
            console.error("Error creating channel:", data.error);
            if (response.status === 401) {
                console.log("Unauthorized access, please log in again.");
                sessionStorage.removeItem("token");
                sessionStorage.setItem("loggedIn", 0);
                window.location.reload();
                setLoggedIn(0);
                console.log("You are logged out, please log in again.");
            } else if (response.status === 404) {
                setError(1);
                console.error("user not found:", data.error);
            }
        }

    } 
    return (
        <div className="playlist-generator-container">
            <h1>Enter your mood</h1>
            <textarea
                className='std-box'
                value={value}
                onChange={(e) => setValue(e.target.value)}
                placeholder='how are you feeling today'
                style={{ resize: 'none' }}
            />
            <button className='std-box' onClick={handleSubmit}><h2>Generate</h2></button>
        </div>
    );
};

export default PlaylistGenerator;