import request from './request';

export async function getRsvList() {
  var rsvList = [];
  let page = 1;
  // eslint-disable-next-line no-constant-condition
  while (true) {
    let { data } = await request.get(`/reservation/?p=${page}`);
    if (data.code !== 0) {
      throw data.errmsg;
    }
    rsvList = [...rsvList, ...data.rsvs];
    if (!data.rsvs.length) {
      break;
    }
    page++;
  }
  return rsvList;
}

export async function submitAudit(id, type, reason) {
  var { data } = await request.post(`/reservation/${id}/`, {
    op: 1,
    pass: type ? 1 : 0,
    reason
  });
  if (data.code !== 0) {
    throw data.errmsg;
  }
  return true;
}

export async function finishRsv(id) {
  var { data } = await request.post(`/reservation/${id}/`, {
    op: 2
  });
  if (data.code !== 0) {
    throw data.errmsg;
  }
  return true;
}
