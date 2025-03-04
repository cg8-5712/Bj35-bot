// api.js

import axios from 'axios';

export async function status() {
    const id = '1309097125891674112';
    
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiSm9obiIsImFkbWluIjp0cnVlfQ.',
    }

    try {
        const response = await axios.get(`${import.meta.env.VITE_APP_API_URL}/device_status/${id}`, {
            headers: headers
        });
        return response.data;
    } catch (error) {
        console.error(error);
        return null;
    }
}