import React from "react"
import { Link } from "react-router-dom"

function HomeButton() {
    return (
        <div>
            <Link to='http://localhost:3000/'>
                <button  className="buttons">home</button>
            </Link>
        </div>
    )
}

export default HomeButton;