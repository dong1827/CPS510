import axios from 'axios';
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';

function Login() {
    /*
    Sending back the content for Login page
    args: None 
    */
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [msg, setMsg] = useState('Welcome to M & P store')
    const navigate = useNavigate()

    const handleSubmit = async (event) => {
        /*
        function for handling form submission/login
        args:
            event: Event of the form
        */
        event.preventDefault();
        //Send username and password to /login to handle the login request
        axios({
            method: "post",
            url: "http://localhost:5000/login",
            withCredentials: true,
            data: {
                username: username,
                password: password
            }  
        })
        .then((response) => {
            if (response.data["login"] == "success") {
                navigate("/");
            }
            else {
                setMsg("Login failed")
            }
        })
        .catch((error) => {
            console.log(error)
        })
    }

    const handleRegisterClick = () => {
        /*
        Navigates to the register page
        args: None
        */
        navigate('/register')
    }

    return (
        <div className={`centerJustified halfHeight`}>
            {/*form for login*/}
            <form id='LRBox' className={`columnFlex solidBorder`} onSubmit={handleSubmit}>
                <div>
                    {/*Username input box*/}
                    <input
                        className='inputBox'
                        placeholder='username'
                        type='text'
                        id='username'
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    {/*Password input box*/}
                    <input
                        className='inputBox'
                        placeholder='password'
                        type='password'
                        id='password'
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                {/*buttons for submit login request and navigating to register page*/}
                <div className='centerJustified'>
                    <button className='buttons' type='submit'>Login</button>
                    <button className='buttons' onClick={handleRegisterClick}>Register</button>
                </div>
                <p className='centerJustified'>{msg}</p>
            </form>
        </div>
    );
}

export default Login;