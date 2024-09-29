import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

export const calculateRoute = async (location, items) => {
    const response = await axios.post(`${API_BASE_URL}/api/calculate`, { location, items });
    return response.data;
};
