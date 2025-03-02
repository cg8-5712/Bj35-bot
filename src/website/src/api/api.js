// api.js
export async function robotId() {
    const id = '1309097125891674112';
    const headers = new Headers();
    headers.append('Accept', 'application/json');
    headers.append('Content-Type', 'application/json');
    headers.append('token', 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiSm9obiIsImFkbWluIjp0cnVlfQ.')
    try {
        const res = await fetch(`http://127.0.0.1:8080/api/v1/device_status/${id}`, {
            method: 'GET',
            headers: headers
        });
        if (!res.ok) {
            throw new Error('NetworkError');
        }

        const res_data = await res.json();

        return res_data['data']['deviceInfo']['deviceId'];

    } catch (error) {
        console.error(error);
        throw error;
    }
}

export async function powerPercent() {
    const id = '1309097125891674112';
    const headers = new Headers();
    headers.append('Accept', 'application/json');
    headers.append('Content-Type', 'application/json');
    headers.append('token', 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiSm9obiIsImFkbWluIjp0cnVlfQ.')
    try {
        const res = await fetch(`http://127.0.0.1:8080/api/v1/device_status/${id}`, {
            method: 'GET',
            headers: headers
        });
        if (!res.ok) {
            throw new Error('NetworkError');
        }

        const res_data = await res.json();

        return res_data['data']['deviceStatus']['powerPercent'];

    } catch (error) {
        console.error(error);
        throw error;
    }
}
