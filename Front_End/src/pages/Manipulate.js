import React, { useState } from 'react'
import axios from 'axios';


function Manipulate() {
    const [result, setResult] = useState("");
    

    const createTable = async () => {
        try {
            const respose = await axios({
                method: "post",
                url: "http://localhost:5000/create",
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
                url: "http://localhost:5000/drop",
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
                <button className='buttons' onClick={createTable}>Create Table</button>
                <button className='buttons' onClick={dropTable}>Drop Table</button>
            </div>
        </div>
    )
}

export default Manipulate;