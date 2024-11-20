import axios from 'axios';
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';

function Register() {
    /*
    Sending back the content for Register page
    args: None 
    */
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [repPassword, setRepPassword] = useState('');
    const [msg, setMsg] = useState('Welcome to M&M Database!');
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        /*
        function for handling form submission/registering the account
        args: 
            event: Event of the form
        */
        event.preventDefault();
        //Check if password and the retyped password match
        try {
            if (password !== repPassword){
                throw new Error('Password do not match')
            };
            //Send data to /register to handle registeration
            const response = await axios.post('https://cps510.onrender.com/register',  { username, password });
            setMsg(response.data['Msg'])
            console.log(response.data);
        } catch (error) {
            setMsg(error.message)
        }
    };

    const handleLoginClick = () => {
        /*
        Navigates to the login page
        args: None
        */
        navigate("/login")
    }

    return (
        <div className={`centerJustified halfHeight`}>
            {/*form for registeration*/}
            <form id='LRBox' className={`columnFlex solidBorder`} onSubmit={handleSubmit}>
                {/*Username input box*/}
                <div>
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

                <div>
                    {/*Retype password input box*/}
                    <input
                        className='inputBox'
                        placeholder='repeat password'
                        type='password'
                        id='repPassword'
                        value={repPassword}
                        onChange={(e) => setRepPassword(e.target.value)}
                        required
                    />
                </div>

                {/*Buttons for navigate to login page and submitting register request*/}
                <div className='centerJustified'>
                    <button className='buttons' type='submit'>Register</button>
                    <button className='buttons' onClick={handleLoginClick}>Login</button>    
                </div>
                <p className='centerJustified'>{ msg }</p>
            </form>
        </div>
    );
}

export default Register;