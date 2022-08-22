import request from './request';
import store from '@/store';

export async function getItemList(session = store.state.session) {
  let page = 1;
  let itemList = [];
  // eslint-disable-next-line no-constant-condition
  while (true) {
    var { data } = await request.get(`/item/?p=${page}`, {
      headers: {
        session
      }
    });
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

export async function getItem(id, session = store.state.session) {
  var { data } = await request.get(`/item/${id}/`, {
    headers: {
      session
    }
  });
  if (data.code !== 0) {
    throw data.errmsg;
  }
  return data.item;
}

export async function postItem(item, session = store.state.session) {
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
  }, {
    headers: {
      session
    }
  });
  if (data.code !== 0) {
    throw data.errmsg;
  }
  return item.id || data['item-id'];
}

export async function deleteItem(id, session = store.state.session) {
  var { data } = await request.delete(`/item/${id}/`, {
    headers: {
      session
    }
  });
  if (data.code !== 0) {
    throw data.errmsg;
  }
  return id;
}