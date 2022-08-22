import request from './request';
import store from '@/store';

function makeRequestParameter(req) {
    var res = [];
    for (const key of Object.keys(req)) {
        if (req[key]) {
            res.push(`${key}=${req[key]}`);
        }
    }
    return res.join('&');
}

export async function getIssueList(params = {}, session = store.state.session) {
    // eslint-disable-next-line no-constant-condition
    var { data } = await request.get(`/issue/?${makeRequestParameter(params)}`, {
        headers: {
            session
        }
    });
    if (data.code !== 0) {
        throw data.errmsg;
    }
    delete data.code;
    delete data.errmsg;
    return data;
}

export async function getIssue(id, session = store.state.session) {
    var { data } = await request.get(`/issue/${id}/`, {
        headers: {
            session
        }
    });
    if (data.code !== 0) {
        throw data.errmsg;
    }
    delete data.code;
    delete data.errmsg;
    return data;
}

export async function createIssue(issue, session = store.state.session) {
    var { data } = await request.post('/issue/', issue, {
        headers: { session }
    });
    if (data.code !== 0) {
        throw data.errmsg;
    }
    return data['issue_id'];
}

export async function postIssue(id, issue, session = store.state.session) {
    var { data } = await request.post(`/issue/${id}/`, issue, {
        headers: { session }
    });
    if (data.code !== 0) {
        throw data.errmsg;
    }
    return true;
}