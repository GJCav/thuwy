import axios from 'axios';
import config from '@/config';

export async function upload(file) {
  let { data: ret1 } = await axios.get(`${config.ServerAddr}/uploadurl/${file.name}`, {
    timeout: 5000,
    responseType: 'json',
    headers: {
      'Content-Type': 'application/json;charset=utf-8'
    }
  });
  if (ret1.code !== 0) {
    throw ret1.msg;
  }
  let { data: url } = ret1;
  let { data: ret2 } = await axios.put(url, file);
  if (ret2 !== '') {
    throw ret2;
  }
  return url.split('?')[0];
}