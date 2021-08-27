import request from './request';

export async function getItemList(page = 1) {
  var { data } = await request.get(`/item/?p=${page}`);
  if (data.code !== 0) {
    throw data.errmsg;
  }
  return data.items;
}

export async function getItem(id) {
  var { data } = await request.get(`/item/${id}`);
  if (data.code !== 0) {
    throw data.errmsg;
  }
  return data.item;
}

export async function postItem(item) {
  var { data } = await request.post(`/item/${item.id}`, {
    name: item.name,
    available: item.available,
    'brief-intro': item['brief-intro'],
    'md-intro': item['md-intro'],
    thumbnail: item.thumbnail,
    'rsv-method': item['rsv-method']
  });
  if (data.code !== 0) {
    throw data.errmsg;
  }
  return true;
}
