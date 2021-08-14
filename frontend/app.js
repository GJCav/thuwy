// app.js
App({
  onLaunch() {
    // 登录
    wx.login({
      timeout: 5000,
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        wx.request({
          url: this.globalData.url + '/login/',
          method: 'POST',
          data: {
            code: res.code
          },
          success: res => {
            if (res.data.code == 0) {
              this.globalData.login = true;
              this.globalData.userInfo = res.data.bound;
              //将得到的openid存储到缓存里面方便后面调用
              wx.setStorage({
                key: "cookie",
                data: res.cookies[0]
              })
              console.log('登陆成功')
            } else {
              console.log(res.data.code, res.data.errmsg);
              wx.showToast({
                title: '登录失败',
                icon: 'error',
                duration: 1500
              });
            }
          }
        })
      }
    });
    if (this.globalData.userInfo) {
      wx.request({
        url: this.globalData.url + '/profile/',
        method: 'GET',
        header: {
          'content-type': 'application/json; charset=utf-8',
          'cookie': wx.getStorageSync('cookie')
        },
        success: (res) => {
          if (res.data.code == 0) {
              this.globalData.isadmin=res.data.admin?true:false
          } else {
            console.log(res.data.code, res.data.errmsg);
            wx.hideLoading();
            wx.showToast({
              title: '信息读取失败',
              icon: 'error',
              duration: 1500,
            })
          }
        },
        fail: (res) => {
          console.log(res.data.code, res.data.errmsg);
          wx.showToast({
            title: '信息读取失败',
            icon: 'error',
            duration: 1500
          });
        }
      })
    }
  },
  globalData: {
    login: false,
    isadmin: true,
    userInfo: false,
    url: "http://api.weiyang.grw20.cn/"
  }
})