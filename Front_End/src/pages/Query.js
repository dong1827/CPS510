import axios from 'axios'
import React, { useState } from 'react'
import DataTable from '../components/DataTable';
import HomeButton from '../components/HomeButton';

function Query() {
    const [msg, setMsg] = useState("");
    const [query, setQuery] = useState("customer");
    const [result, setResult] = useState("");
    const [rows, setRows] = useState("");
    const [cols, setCols] = useState("");
    

    const fetchQuery = async () => {
        setMsg("Loading...");
        try {
            
            const respose = await axios({
                method: "post",
                url: "https://visually-talented-grubworm.ngrok-free.app/query",
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
            <label htmlFor='query'>Select a table to view:</label>
            <select id="query" value={query} onChange={selectQuery}>
                <option value="customer">Customers</option>
                <option value="employee">Employee</option>
                <option value="product">Products</option>
                <option value="genre">Genre</option>
                <option value="movie">Movie</option>
                <option value="music">Music</option>
                <option value="records">Records</option>
                <option value="review">Review</option>
                <option value="stocks">Stocks</option>
                <option value="storecredit">StoreCredit</option>
                <option value="stores">Stores</option>
            </select>
        
            <button className='buttons' onClick={fetchQuery}>Select</button>

            <div>
                <p>{msg}</p>
                <p>{result}</p>
                <DataTable columns={cols} rows={rows}/>
            </div>
            
            
        </div>
    )
}

export default Query;