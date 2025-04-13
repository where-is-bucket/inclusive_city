import axios from "axios";
import {WEB_API_BASE_URL} from './../config';

const BASE_URL = WEB_API_BASE_URL;

export const getPlaces = () => {
    return axios.get(`${BASE_URL}/places`, {
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
        },
    });
}

export const getFacilities = () => {
    return axios.get(`${BASE_URL}/facilities`);
}

export const getPlaceById = ({ params }) => {
    return axios.get(`${BASE_URL}/places/${params.place_id}`, );
}

export const getReviewsByMarkerId = ({ params }) => {
    return axios.get(`${BASE_URL}/places/${params.place_id}/reviews`);
}

export const addReview =({ payload }) => {
    return axios.post(`${BASE_URL}/reviews`, payload);
}

export const addFacility =({ params }) => {
    return axios.put(`${BASE_URL}/place/${params.place_id}/facilities/${params.place_id}`);
}

export const removeFacility =({ params }) => {
    return axios.delete(`${BASE_URL}/place/${params.place_id}/facilities/${params.place_id}`);
}