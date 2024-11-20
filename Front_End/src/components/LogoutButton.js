import axios from "axios";
import React from "react";
import { useLocation, useNavigate } from "react-router-dom";


function LogoutButton() {
    const navigate = useNavigate();
    const location = useLocation();

    const handleLogout= async () => {
        try {
            const response = await axios({
                method: "post",
                url: "http://localhost:5000/logout",
                withCredentials: true
            });

            const data = response.data; 
            if (data["result"] == "success") {
                if ("/" == location.pathname) {
                    window.location.reload();
                }
                navigate("/")
            }
        }
        catch (err) {
            console.log(err);
        }
    }

    return(
        <button className={`buttons rightJustified`} onClick={ handleLogout }>Logout</button>
    )
}

export default LogoutButton;