import React from 'react'
import '../styles/LandingPage.css'
import Header from './Header'

const LandingPage = () => {

    const handleLogin = () => {
        window.location.href = 'http://localhost:5000/login'; // Redirect to backend login route
    }

  return (
    <>  
    <Header/>
    <div className='landing-page-container'>
        <div className="landing-page-content-container">
            <div className='landing-page-content std-box'>
                <h1>
                    Create the perfect playlist in seconds 
                </h1>
                <h3>
                    Use ai to create perfect playlists for your specific mood in just a few seconds
                </h3>
            </div>
        </div>

        <div className="landing-page-cta std-box">
            <button className='std-box' onClick={handleLogin}><h1>Get Started</h1></button>
        </div>
        <div className='landing-page-grid'></div>
        <div className='landing-page-grid-mask'></div>
        <div className="landing-page-red-box extra-box std-box"></div>
        <div className="landing-page-purple-box extra-box std-box"></div>
    </div>
    </>
     )
}

export default LandingPage
