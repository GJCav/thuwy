import request from './request';

export async function getUserProfile() {
  var { data } = await request.get('/profile/');
  console.log(data);
  if (data.code !== 0) {
    throw (data.errmsg);
  }
  let result = {
    name: data.name,
    clazz: data.clazz,
    id: data['school-id'],
    admin: data.admin
  };
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