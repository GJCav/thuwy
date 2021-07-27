// index.js
// 获取应用实例
const app = getApp()

Page({
  data: {
    motto1: ["未认证用户", "普通用户", "管理员"],
    motto2: ['未绑定', '已绑定'],
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
    if (app.globalData.userInfo) {
      this.setData({
        num1:1,
        num2:1
      })
    }
    else{
      this.setData({
        num1:0,
        num2:0
      })
    }
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
    wx.navigateTo({
      url: '../bind/bind'
    })
  }
})