import axios from 'axios';
import config from '@/config';

const request = axios.create({
  baseURL: config.BackAPIAddr,
  timeout: 5000,
  responseType: 'json',
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  },
  withCredentials: true
});

export default request;