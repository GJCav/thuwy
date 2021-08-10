// setting.js
const app = getApp()

Page({
  data: {
    motto1: ['未登录', '未认证用户', '普通用户', '管理员','违约用户'],
    motto2: ['—', '未绑定', '已绑定'],
    selection: [{
      text: "绑定账户信息",
      go: "bindinfo"
    }, {
      text: "申请成为管理员",
      go: "beadmin"
    }, {
      text: "反馈问题和建议",
      go: ""
    }],
    num1: 0,
    num2: 0,
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    canIUseGetUserProfile: false,
    canIUseOpenData: wx.canIUse('open-data.type.userAvatarUrl') && wx.canIUse('open-data.type.userNickName')
  },
  onLoad() {
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
    wx.setNavigationBarTitle({
      title: '个人管理'
    })
  },
  onShow() {
    if (app.globalData.login) {
      if (app.globalData.userInfo) {
        this.setData({
          num1: 2,
          num2: 2
        })
      } else {
        this.setData({
          num1: 1,
          num2: 1
        })
      }
    } else {
      this.setData({
        num1: 0,
        num2: 0
      })
    }
    if(app.globalData.isadmin)  
    this.setData({
      num1: 3,
    })
  },
  getUserProfile(e) {
    wx.getUserProfile({
      desc: '展示用户信息',
      success: (res) => {
        console.log(res)
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    })
  },
  bindinfo() {
    if (app.globalData.login == false) {
      wx.showToast({
        title: '未成功登录',
        icon: 'error',
        duration: 1500
      })
    } else if (app.globalData.userInfo) {
      wx.showToast({
        title: '您已绑定信息',
        icon: 'error',
        duration: 1500
      })
    } else {
      wx.navigateTo({
        url: '../bind/bind'
      })
    }
  },
  beadmin() {
    wx.showLoading({
      mask: true,
      title: '申请中',
    })
    wx.request({
      url: app.globalData.url + '/admin/',
      method: 'POST',
      header: {
        'content-type': 'application/json; charset=utf-8',
        'cookie': wx.getStorageSync('cookie')
      },
      success: (res) => {
        if (res.data.code == 0) {
          wx.hideLoading();
          wx.showToast({
            title: '提交申请成功',
            icon: 'success',
            duration: 1500,
          })
        } else {
          console.log(res.data.code, res.data.errmsg);
          wx.hideLoading();
          wx.showToast({
            title: '申请失败',
            icon: 'error',
            duration: 1500,
          })
        }
      },
      fail: (res) => {
        console.log(res.data.code, res.data.errmsg);
        wx.hideLoading();
        wx.showToast({
            title: '连接失败',
            icon: 'error',
            duration: 1500
        });
    }
    })

  }
})