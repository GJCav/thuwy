// app.js
App({
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
                  key: "cookie",
                  data: res.cookies[0]
                })
                if (that.globalData.userInfo) {
                  wx.request({
                    url: that.globalData.url + '/profile/',
                    method: 'GET',
                    header: {
                      'content-type': 'application/json; charset=utf-8',
                      'cookie': res.cookies[0]
                    },
                    success: (res) => {
                      if (res.data.code == 0) {
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
    login: false,
    isadmin: false,
    userInfo: false,
    item_feature: [{
      title: '自动通过审批',
      text: '在预约提交成功的情况下，系统会自动完成审批。适用于29号楼会议室等不需要管理员特别审批的物品。'
    }],
    item_group:['全部物品','设备器材','公共活动室','其他物品'],
    url: 'https://api.thuwy.top', //本地测试地址：'http://127.0.0.1:5000'
    picurl: 'https://web.thuwy.top/api',
    webBackendUrl: 'https://web.thuwy.top/api'
  }
})