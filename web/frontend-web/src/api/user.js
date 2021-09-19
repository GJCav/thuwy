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

export async function getAllUsers() {
  var { data } = await request.get('/user/');
  if (data.code == 0) {
    return data.profiles;
  } else {
    throw (data.errmsg);
  }
}

export async function revokeAdmin(openid) {
  var { data } = await request.delete(`/admin/${openid}/`);
  if (data.code != 0) {
    throw (data.errmsg);
  }
}

export async function unbindUser(openid) {
  var { data } = await request.delete(`/user/${openid}/`);
  if (data.code != 0) {
    throw (data.errmsg);
  }
}

export async function getAdminRequestList() {
  var { data } = await request.get('/admin/request/');
  if (data.code == 0) {
    return data.list;
  } else {
    throw (data.errmsg);
  }
}

export async function auditAdminRequest(requestId, reason = '', pass = 0) {
  var { data } = await request.post(`/admin/request/${requestId}/`, {
    reason,
    pass
  });
  if (data.code != 0) {
    throw (data.errmsg);
  }
}
