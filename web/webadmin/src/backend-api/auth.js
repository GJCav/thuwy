import * as base from "./url"
import urlcat from "urlcat";

//////////////////////////////////////////////////////////
//
// 用户管理
//

export const fetchMyProfile = async ({ session }) => {
  const url = base.api("/profile/");
  const res = await fetch(url, {
    headers: { session }
  })
  if (res.status !== 200) {
    throw new Error(`fetchMyProfile: HTTP error: ${res.status}`);
  }

  const json = await res.json();
  return json;
}


export const fetchUserProfile = async ({ session, openid }) => {
  const url = base.api("/profile/" + openid + "/")
  const res = await fetch(url, { headers: { session }})
  if (res.status != 200) throw new Error(`fetchUserProfile: HTTP error: ${res.status}`);
  return await res.json();
}


export const fetchUserList = async ({ session, clazz, p, name }) => {
  const url = urlcat(base.api("/user/"), { clazz, p, name })
  const res = await fetch(url, { headers: { session } })
  if (res.status !== 200) {
    throw new Error(`fetchUserList: HTTP error: ${res.status}`)
  }
  const json = await res.json()
  return json
}


//////////////////////////////////////////////////////////
//
// 用户权限管理
//

export const getAllPrivileges = (privilege_info) => {
  let privilegeSet = []
  
  privilegeSet = privilegeSet.concat(privilege_info.privileges)
  for (const groupName in privilege_info.group_privileges) {
    privilegeSet = privilegeSet.concat(privilege_info.group_privileges[groupName])
  }

  return Array.from(new Set(privilegeSet));
}

export const fetchUserDetailedPrivilegeInfo = async ({ session, openid }) => {
  const url = base.api(`/user/${openid}/scope/`)
  const res = await fetch(url, { headers: { session }})
  if (res.status !== 200) throw new Error(`fetchUserDetailedPrivilegeInfo: HTTP error: ${res.status}`);
  return await res.json()
}


export const fetchAllScope = async ({ session }) => {
  const url = base.api("/auth/scope/");
  const res = await fetch(url, { headers: { session }})
  if (res.status !== 200) 
    throw new Error(`fetchAllScope: HTTP error: ${res.status}`);
  return await res.json();
}


export const addUserScope = async ({ session, name, openid, expire_at }) => {
  const url = urlcat(base.API_URL + "/user/:openid/scope/", { openid })
  const res = await fetch(url, { 
    method: "POST",
    headers: { 
      session,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ scope: name, expire_at: expire_at || 0 })
  })
  if (res.status !== 200) 
    throw new Error(`addUserScope: HTTP error: ${res.status}`);
  return await res.json()
}


export const delUserScope = async ({ session, name, openid }) => {
  const url = urlcat(base.api("/user/:openid/scope/:name/"), {
    name, openid
  })
  const res = await fetch(url, {
    method: "delete",
    headers: { session }
  })
  if (res.status !== 200){
    throw new Error(`delUserScope: HTTP error: ${res.status}`)
  }
  return await res.json();
}


//////////////////////////////////////////////////////////
//
// 用户组管理
//

export const fetchGroupList = async ({ session, regex, p }) => {
  const url = urlcat(base.API_URL + "/auth/group/", { regex, p })
  const res = await fetch(url, { headers: { session }})
  if (res.status !== 200) {
    throw new Error(`fetchGroupList: HTTP error: ${res.status}`);
  }
  return await res.json();
}


export const delGroup = async ({ session, name }) => {
  const url = urlcat(base.API_URL + "/auth/group/:name/", { name })
  const res = await fetch(url, {
    method: "delete",
    headers: { session }
  })
  if (res.status !== 200) {
    throw new Error(`delGroup: HTTP error: ${res.status}`);
  }
  return await res.json();
}


export const addGroup = async ({ session, name, expire_at }) => {
  const url = base.api("/auth/group/")
  const res = await fetch(url, {
    method: "post",
    headers: {
      session,
      "content-type": "application/json"
    },
    body: JSON.stringify({ name, expire_at })
  })
  if (res.status !== 200) {
    throw new Error(`addGroup: HTTP error: ${res.status}`);
  }
  return await res.json();
}


export const fetchGroupInfo = async ({ session, name }) => {
  const url = urlcat(base.api("/auth/group/:name/"), { name })
  const res = await fetch(url, { headers: { session }})
  if (res.status !== 200) {
    throw new Error(`fetchGroupInfo: HTTP error: ${res.status}`);
  }
  return await res.json();
} 


export const addGroupMember = async ({ session, openid, group_name }) => {
  const url = urlcat(
    base.api("/auth/group/:group_name/member/"),
    { group_name }
  )
  const res = await fetch(url, {
    method: 'post',
    headers: {
      session,
      "content-type": "application/json"
    },
    body: JSON.stringify({ openid })
  })
  if (res.status !== 200) {
    throw new Error(`addGroupMember: HTTP error: ${res.status}`);
  }
  return await res.json()
}


export const delGroupMember = async ({ session, openid, group_name}) => {
  const url = urlcat(
    base.api("/auth/group/:group_name/member/:openid/"),
    { group_name, openid }
  )
  const res = await fetch(url, {
    method: 'delete',
    headers: { session },
  })
  if (res.status !== 200) {
    throw new Error(`delGroupMember: HTTP error: ${res.status}`);
  }
  return await res.json()
}


export const addGroupScope = async ({ session, scope, group_name }) => {
  const url = urlcat(
    base.api("/auth/group/:group_name/scope/"),
    { group_name }
  )
  const res = await fetch(url, {
    method: 'post',
    headers: {
      session,
      "content-type": 'application/json'
    },
    body: JSON.stringify({ scope })
  })
  if (res.status !== 200) {
    throw new Error(`addGroupScope: HTTP error: ${res.status}`);
  }

  return await res.json();
}


export const delGroupScope = async ({ session, scope, group_name }) => {
  const url = urlcat(
    base.api("/auth/group/:group_name/scope/:scope/"), {
      group_name, scope
    }
  );
  const res =  await fetch(url, {
    method: 'delete',
    headers: { session }
  })
  if (res.status !== 200) {
    throw new Error(`delGroupScope: HTTP error: ${res.status}`);
  }
  return await res.json()
}