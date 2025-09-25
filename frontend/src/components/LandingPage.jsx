import React from 'react'
import '../styles/LandingPage.css'

const LandingPage = () => {
  return (
    <>  
    <div className='landing-page-container'>
            <div className="landing-page-content-container">
            <div className='landing-page-content std-box'>
                <h1>
                    Moodify.
                </h1>
                <h3>
                    Create the perfect playlist for your mood.
                </h3>
            </div>
        </div>

        <div className="landing-page-cta std-box">
            <button className='std-box'><h2>Get Started</h2></button>
        </div>

    </div>
    </>
     )
}

export default LandingPage
