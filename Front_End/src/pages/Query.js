import axios from 'axios'
import React, { useState } from 'react'

function Query() {
    const [msg, setMsg] = useState("Select your query");
    const [query, setQuery] = useState("");
    const [result, setResult] = useState("");
    

    const fetchQuery = async () => {
        try {
            const respose = await axios({
                method: "post",
                url: "http://localhost:5000//Query",
                withCredentials: true,
                data: {
                    query: query
                }
            });

            const data = respose.data;
        
            if (data["result"] != "") {
                setResult(data["result"]);
            }
            else {
                setResult("Empty");
            }

        }
        catch (err) {
            console.log(err);
        }
    }

    const selectQuery = (event) => {
        setQuery(event.target.value);
    };


    return (
        <div>
            <label htmlFor='query'>Select a table to view:</label>
            <select id="query" value={query} onChange={selectQuery}>
                <option value="customers">Customers</option>
                <option value="products">Products</option>
                <option value="storecredits">StoreCredits</option>
            </select>
        
            <button className='buttons' onClick={fetchQuery}>Select</button>
        </div>
    )
}

export default Query;