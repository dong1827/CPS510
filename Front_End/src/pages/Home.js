import axios from 'axios';
import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom';
import LRButtons from '../components/LRButtons';
import LogoutButton from '../components/LogoutButton';

//Start button to redirect the user to choosing their game
function QueryButton() {
    return (
        <div> 
            <Link to='query'>
                <button className='buttons'>Query</button>
            </Link>
        </div>
    )
}

function AdvQueryButton() {
    return (
        <div> 
            <Link to='advQuery'>
                <button className='buttons'>Advanced Query</button>
            </Link>
        </div>
    )
}

function InsertButton() {
    return (
        <div> 
            <Link to='insert'>
                <button className='buttons'>Insert</button>
            </Link>
        </div>
    )
}

function ManipulateButton() {
    return (
        <div> 
            <Link to='manipulate'>
                <button className='buttons'>Create/Drop</button>
            </Link>
        </div>
    )
}

function WelcomeHeader({user}) {

    return (
        <div id='welcomePage' className='centerJustified'>

            <div className={`rightJustified highPadding`}>
                {user 
                ? <div id="userInfo">
                    <label id="user">Welcome: { user }</label>
                    <LogoutButton></LogoutButton>
                </div> 

                : <LRButtons />}
            </div>

            <div className={`centerJustified columnFlex fullWidth`}>
                <h1>Welcome to M&M Database<br></br>
                    {user 
                    ? <span> Select one of the options below</span> 
                    : <span> Please login using the buttons on the top right.</span>}
                </h1>
                
                <div className='rowFlex'> 
                    <QueryButton />
                    <AdvQueryButton />
                    <ManipulateButton />
                    <InsertButton />
                </div>
                
            </div>
        </div>
    )
}

function HomePage() {
    
    return (
        <div id='homePage'>
            
        </div>
    )
}


function Home() {
    //Check if there's an active session
    const [user, setUser] = useState(null)
    const [points, setPoints] = useState(0)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        //Getting the current user 
        const fetchUser = async () => {
            try {
                const response = await axios({
                    method: "get",
                    url: ("https://visually-talented-grubworm.ngrok-free.app/session"),
                    withCredentials: true
                });

                const data = response.data;

                if (data["session"] != "None" && data["session"] != user) {
                    setUser(data["session"]);
                    setPoints(data["points"]);
                }
            }
            catch (err) {
                console.log(err)
            }
            finally {
                setLoading(false)
            }
            
        }

        fetchUser();
        
    }, [user, points]);     

    if (loading) {
        return (
            <p>Loading...</p>
        )
    }

    return(
        <div>
            <WelcomeHeader user={user}/>
            <HomePage></HomePage>
        </div>
    )
    
}

export default Home;