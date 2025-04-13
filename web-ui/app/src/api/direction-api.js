import axios from "axios";
import {MANAGEMENT_API_BASE_URL} from './../config';

const BASE_URL = MANAGEMENT_API_BASE_URL;

export const getRoute = ({payload}) => {
    return axios.post(`${BASE_URL}/route`, payload);
}
