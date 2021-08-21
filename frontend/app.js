// app.js
App({
  getUserInfo() {
    let that=this
    return new Promise(function (resolve, reject) {
      wx.login({ // 登录
        timeout: 5000,
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
                      'cookie': wx.getStorageSync('cookie')
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
                }
                resolve()
              } else {
                reject(res)
              }
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
    url: "http://127.0.0.1:5000/",//http://api.weiyang.grw20.cn
    picurl: "http://static.weiyang.grw20.cn/api/"
  }
})