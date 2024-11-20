import React, { useState } from 'react'
import axios from 'axios';


function Insert() {
    const [result, setResult] = useState("");

    const dummyData = async () => {
        try {
            const respose = await axios({
                method: "post",
                url: "https://cps510.onrender.com/dummyData",
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

    const dropTable = async () => {
        try {
            const respose = await axios({
                method: "post",
                url: "https://cps510.onrender.com/drop",
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
            <div className='centerJustified columnFlex'>
                <p>Select your action</p>
                <p>{result}</p>
            </div>
            <div className='centerJustified'>
                <button className='buttons' onClick={dummyData}>Insert Dummy Data</button>
                <button className='buttons' onClick={dropTable}>Insert</button>
            </div>
        </div>
    )
}

export default Insert;