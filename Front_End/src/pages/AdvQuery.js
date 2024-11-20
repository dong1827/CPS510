import axios from 'axios'
import React, { useState } from 'react'
import DataTable from '../components/DataTable';
import HomeButton from '../components/HomeButton';

function AdvQuery() {
    const [msg, setMsg] = useState("");
    const [query, setQuery] = useState("0");
    const [result, setResult] = useState("");
    const [rows, setRows] = useState("");
    const [cols, setCols] = useState("");
    

    const fetchAdvQuery = async () => {
        setMsg("Loading...");
        try {
            
            const respose = await axios({
                method: "post",
                url: "https://visually-talented-grubworm.ngrok-free.app/advQuery",
                withCredentials: true,
                data: {
                    query: query
                }
            });

            const data = respose.data;
        
            if (data["result"] != "") {
                setResult(data["result"]);
                setRows(data["rows"]);
                setCols(data["columns"]);
            }
            else {
                setResult("Empty");
            }

            console.log(data["columns"])
            console.log(data["rows"])

        }
        catch (err) {
            console.log(err);
        }
        setMsg("");
    }

    const selectQuery = (event) => {
        setQuery(event.target.value);
    };


    return (
        <div>
            <HomeButton />
            <h2>Select your query</h2>
            <label htmlFor='AdvQuery'>Select a table to view:</label>
            <select id="AdvQuery" value={query} onChange={selectQuery}>
                <option value="0">Query 1: Customers who have Purchased Both Movies and Music</option>
                <option value="1">Query 2: Customers Who Either Left a Review or Made a Purchase</option>
                <option value="2">Query 3: Stores with More Than 2 Transactions</option>
                <option value="3">Query 4: Products with Reviews but Not Purchased by 'john_doe'</option>
                <option value="4">Query 5: Average Price of Music and Movies in Each Store</option>
            </select>
        
            <button className='buttons' onClick={fetchAdvQuery}>Select</button>

            <div>
                <p>{msg}</p>
                <p>{result}</p>
                <DataTable columns={cols} rows={rows}/>
            </div>
            
            
        </div>
    )
}

export default AdvQuery;