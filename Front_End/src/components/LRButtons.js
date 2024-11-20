import React from "react";
import { Link } from "react-router-dom";

function LRButtons() {
    return (
        <div>
            <Link to='http://localhost:3000/login'>
                <button className="buttons">Login</button>
            </Link>

            <Link to='http://localhost:3000/register'>
                <button className="buttons">Register</button>
            </Link>
        </div>
    );
}

export default LRButtons;