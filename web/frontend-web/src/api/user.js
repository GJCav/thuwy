import request from './request';

export async function getUserProfile(session) {
  var { data } = await request.get('/profile/', {
    headers: { session }
  });

  console.log(data);

  if (data.code !== 0) {
    throw (data.errmsg);
  }
  delete data.code;
  delete data.errmsg;
  return data;
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
