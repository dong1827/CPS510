import React, { useState } from 'react'
import axios from 'axios';
import HomeButton from '../components/HomeButton';

function Insert() {
    const [result, setResult] = useState("");
    const [msg, setMsg] = useState("");

    // Send server a insert dummy data request
    const dummyData = async () => {
        setMsg("loading...");
        try {
            const respose = await axios({
                method: "post",
                url: "https://visually-talented-grubworm.ngrok-free.app/dummyData",
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
    }

    return (
        <div className='columnFlex'>
            <HomeButton />
            
            {/*Interface for insert data*/}
            <div className='centerJustified columnFlex'>
                <p>Select your action</p>
                <p>{msg}</p>
                <p>{result}</p>
            </div>
            <div className='centerJustified'>
                <button className='buttons' onClick={dummyData}>Insert Dummy Data</button>
            </div>
        </div>
    )
}

export default Insert;