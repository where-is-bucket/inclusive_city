import axios from "axios";

const BASE_URL = import.meta.env.VITE_ROUTE_MANAGEMENT_API_BASE_URL;

export const getRoute = ({payload}) => {
    return axios.post(`${BASE_URL}/route`, payload);
}
