import React from "react";
import { Link } from "react-router-dom";

function LRButtons() {
    return (
        <div>
            <Link to='login'>
                <button className="buttons">Login</button>
            </Link>

            <Link to='register'>
                <button className="buttons">Register</button>
            </Link>
        </div>
    );
}

export default LRButtons;