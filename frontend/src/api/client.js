const API_BASE = `http://${window.location.hostname}:8000/api`;

const apiClient = {
    async get(endpoint, options = {}) {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API request failed');
        }
        return response.json();
    },

    async post(endpoint, body, options = {}) {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            body: JSON.stringify(body),
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API request failed');
        }
        return response.json();
    }
};

export default apiClient;
