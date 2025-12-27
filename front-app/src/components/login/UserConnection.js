import './UserConnection.css';
import { Link } from 'react-router-dom';

export default function UserConnection() {

    return (
        <div className="user-connection-container">
            <Link to="/login" className="user-connection-link">Login</Link>
            <Link to="/register" className="user-connection-link">Register</Link>
        </div>
    );
}