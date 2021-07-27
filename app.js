// app.js
App({
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        wx.request({
          url: this.globalData.url+'/login',
          method:'POST',
          data:{
            code:res.code
          },
          success: function (res) {
            console.log('登录请求成功');
            this.globalData.userInfo=res.bound;
            if(res.code==0){
              wx.setStorage({ //将得到的openid存储到缓存里面方便后面调用
              key: "openid",
              data: res.data.openid
              })
            }
            else {
              console.log(res.code,res.errmsg);
              wx.showToast({
                title: '登录失败',
                icon: 'error',
                duration: 1500
              });
            }
          }
        })
      } 
    })
  },
  globalData:{
    userInfo: false,
    url: "这是服务器url"
  }
})
