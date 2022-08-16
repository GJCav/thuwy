// app.js
App({
  towxml:require('/towxml/index'),
  getUserInfo() {
    let that = this
    return new Promise(function (resolve, reject) {
      wx.login({ // 登录
        timeout: 10000,
        success: res => { // 发送 res.code 到后台换取 openId, sessionKey, unionId
          wx.request({
            url: that.globalData.url + '/login/',
            method: 'POST',
            data: {
              code: res.code
            },
            success: res => {
              if (res.data.code == 0) {
                that.globalData.login = true;
                that.globalData.userInfo = res.data.bound;
                wx.setStorage({ //将得到的openid存储到缓存里面方便后面调用
                  key: "Session",
                  data: res.header["Session"]
                })
                if (that.globalData.userInfo) {
                  wx.request({
                    url: that.globalData.url + '/profile/',
                    method: 'GET',
                    header: {
                      'content-type': 'application/json; charset=utf-8',
                      'Session': wx.getStorageSync("Session")
                    },
                    success: (res) => {
                      if (res.data.code == 0) {
                        that.globalData.school_id=res.data['school-id']
                        that.globalData.isadmin = res.data.admin ? true : false
                        resolve()
                      } else {
                        reject(res)
                      }
                    },
                    fail: (res) => {
                      reject(res)
                    }
                  })
                } else{
                  resolve()
                }
              } else {
                reject(res)
              }
            },
            fail:res=>{
              reject(res)
            }
          })
        },
        fail: res => {
          reject(res)
        }
      });
    })
  },
  globalData: {
    school_id:'',
    login: false,
    isadmin: false,
    userInfo: false,
    item_feature: [{
      title: '自动通过审批',
      text: '在预约提交成功的情况下，系统会自动完成审批。适用于29号楼会议室等不需要管理员特别审批的物品。'
    }],
    item_group:['全部物品','未央设备','29号楼','其他物品'],
    url: 'https://dev-api.thuwy.top', //本地测试地址：'http://127.0.0.1:5000'https://api.thuwy.top
    picurl: 'https://web.thuwy.top/api',
    webBackendUrl: 'http://39.105.175.237:8500'
  }
})