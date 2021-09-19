import request from './request';

export async function getItemList() {
  let page = 1;
  let itemList = [];
  // eslint-disable-next-line no-constant-condition
  while (true) {
    var { data } = await request.get(`/item/?p=${page}`);
    if (data.code !== 0) {
      throw data.errmsg;
    }
    itemList = [...itemList, data.items];
    if (data.items.length < 20) {
      break;
    }
  }
  return data.items;
}

export async function getItem(id) {
  var { data } = await request.get(`/item/${id}/`);
  if (data.code !== 0) {
    throw data.errmsg;
  }
  return data.item;
}

export async function postItem(item) {
  let url = item.id === 0 ? '/item/' : `/item/${item.id}/`;
  var { data } = await request.post(url, {
    name: item.name,
    available: item.available,
    'brief-intro': item['brief-intro'],
    'md-intro': item['md-intro'],
    thumbnail: item.thumbnail,
    'rsv-method': item['rsv-method'],
    attr: item.attr,
    group: item.group
  });
  if (data.code !== 0) {
    throw data.errmsg;
  }
  return item.id || data['item-id'];
}

export async function deleteItem(id) {
  var { data } = await request.delete(`/item/${id}/`);
  if (data.code !== 0) {
    throw data.errmsg;
  }
  return id;
}