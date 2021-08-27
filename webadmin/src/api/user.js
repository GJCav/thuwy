import request from './request';
import store from '@/store';

export async function getUserProfile() {
  var ret = await request.get('/profile/');
  let data = ret.data;
  if (ret.code !== 0) {
    throw (ret.errmsg);
  }
  let result = {
    name: data.name,
    clazz: data.clazz,
    id: data['school-id'],
    admin: data.admin
  };
  store.commit('setUser', result);
  return result;
}

export async function Login(code) {
  var ret = await request.post('/login/', {
    code
  });
  let data = ret.data;
  if (data.code == 0) {
    return true;
  } else {
    throw (data.errmsg);
  }
}