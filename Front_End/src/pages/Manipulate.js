import React, { useState } from 'react'
import axios from 'axios';
import HomeButton from '../components/HomeButton';

function Manipulate() {
    const [result, setResult] = useState("");
    const [msg, setMsg] = useState("");

    const createTable = async () => {
        setMsg("Loading...");
        try {
            const respose = await axios({
                method: "post",
                url: "https://visually-talented-grubworm.ngrok-free.app/create",
                withCredentials: true,
            });

            const data = respose.data;
        
            if (data["result"] != "") {
                setResult(data["result"]);
            }
        }
        catch (err) {
            console.log(err);
        }

        setMsg("");
    }

    const dropTable = async () => {
        setMsg("Loading...");
        try {
            const respose = await axios({
                method: "post",
                url: "https://visually-talented-grubworm.ngrok-free.app/drop",
                withCredentials: true,
            });

            const data = respose.data;
        
            if (data["result"] != "") {
                setResult(data["result"]);
            }
        }
        catch (err) {
            console.log(err);
        }
        setMsg("");
    }

    return (
        <div className='columnFlex'>
            <HomeButton />
            <div className='centerJustified columnFlex'>
                <p>Select your action</p>
                <p>{msg}</p>
                <p>{result}</p>
            </div>
            <div className='centerJustified'>
                <button className='buttons' onClick={createTable}>Create Table</button>
                <button className='buttons' onClick={dropTable}>Drop Table</button>
            </div>
        </div>
    )
}

export default Manipulate;