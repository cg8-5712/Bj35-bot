// api.js
export async function status() {
    const id = '1309097125891674112';
    const headers = new Headers();
    headers.append('Accept', 'application/json');
    headers.append('Content-Type', 'application/json');
    headers.append('token', 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiSm9obiIsImFkbWluIjp0cnVlfQ.')
    try {
        const res = await fetch(`${import.meta.env.VITE_APP_API_URL}/${id}`, {
            method: 'GET',
            headers: headers
        });
        if (!res.ok) {
            throw new Error('NetworkError');
        }

        const res_data = await res.json();

        return res_data;

    } catch (error) {
        console.error(error);
        throw error;
    }
}