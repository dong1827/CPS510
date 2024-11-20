import axios from "axios";
import React, { FC, useState, useEffect } from "react";
import HomeButton from "./HomeButton";
import LRButtons from "./LRButtons";
import LogoutButton from "./LogoutButton";

interface HeaderProps {
}

//Header that contains user info or redirect to login/register page
const Header: FC<HeaderProps> = ({}) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    //Getting the active session and user's points
    useEffect(() => {
        const fetchInfo = async () => {
            try {
                const response = await axios({
                    method: "get",
                    url: ("https://visually-talented-grubworm.ngrok-free.app/session"),
                    withCredentials: true
                });
                
                const data = response.data;
                console.log(data)
                if (data["session"] != "None" && data["session"] != user) {
                    setUser(data["session"]);
                }
            }
            catch (err) {
                console.log(err);
            }
            finally {
                setLoading(false);
            }
        }    
        
        fetchInfo();
    }, []);     

    if (loading) {
        return (
            <p>Loading...</p>
        )
    }
    else if (user) {
        return (
            <div id="header">
                <HomeButton></HomeButton>
                <div id="userInfo">
                    <label id="user">Welcome: { user }</label>
                    <LogoutButton></LogoutButton>
                </div>    
            </div>
        )
    }
    else {
        return (
            <div>
                <LRButtons></LRButtons>
            </div>
        
        )
    }
}

export default Header;