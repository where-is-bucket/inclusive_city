import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const getPlaces = () => {
    return axios.get(`${BASE_URL}/places`);
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