import * as base from "./url"
import urlcat from "urlcat";

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

export const fetchUserList = async ({ session, clazz, p, name }) => {
  const url = urlcat(base.api("/user/"), { clazz, p, name })
  const res = await fetch(url, { headers: { session } })
  if (res.status !== 200) {
    throw new Error(`fetchUserList: HTTP error: ${res.status}`)
  }
  const json = await res.json()
  return json
}

export const getAllPrivileges = (privilege_info) => {
  let privilegeSet = []
  
  privilegeSet = privilegeSet.concat(privilege_info.privileges)
  for (const groupName in privilege_info.group_privileges) {
    privilegeSet = privilegeSet.concat(privilege_info.group_privileges[groupName])
  }

  return Array.from(new Set(privilegeSet));
}