// setting.js
const app = getApp()
const util = require('../../utils/util.js') 
Page({
  data: {
    index:0,

    motto1: ['未登录', '未认证用户', '普通用户', '管理员', '违约用户'],
    motto2: ['—', '未绑定', '已绑定'],
    select: [{
      text: "绑定账户信息",
      go: "bindinfo",
      condition: true
    }, {
      text: "申请成为管理员",
      go: "beadmin",
      condition: true
    }, {
      text: "进入管理员界面",
      go: "goadmin",
      condition: false
    }, {
      text: "扫码登录网页端",
      go: "scanQR",
      condition: true
    }, {
      text: "反馈问题和建议",
      go: "advice",
      condition: true
    }, {
      text: "退出小程序登录",
      go: "quit",
      condition: true
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
    this.setData({
      'select[0].condition': !app.globalData.userInfo,
      'select[1].condition': !app.globalData.isadmin,
      'select[2].condition': app.globalData.isadmin
    })
    if (app.globalData.login) {
      if (app.globalData.userInfo) {
        this.setData({
          num1: 2,
          num2: 2,
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
    if (app.globalData.isadmin)
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
  //进入管理员界面
  goadmin() {
    wx.navigateTo({
      url: '../admin/admin',
    })
  },
  //绑定信息
  bindinfo() {
    if (app.globalData.login == false) {
      wx.showToast({
        title: '未成功登录',
        icon: 'error',
        duration: 1500,
        mask:true
      })
    } else if (app.globalData.userInfo) {
      wx.showToast({
        title: '您已绑定信息',
        icon: 'error',
        duration: 1500,
        mask:true
      })
    } else {
      wx.navigateTo({
        url: '../bind/bind'
      })
    }
  },
  //申请成为管理员
  beadmin() {
    if (app.globalData.login == false) {
      wx.showToast({
        title: '未成功登录',
        icon: 'error',
        duration: 1500,
        mask:true
      })
    } else {
      wx.showLoading({
        mask: true,
        title: '申请中',
      })
      if (app.globalData.isadmin) {
        wx.hideLoading();
        wx.showToast({
          title: '您已成为管理员',
          icon: 'error',
          duration: 1000,
          mask:true
        })
      }
      if (app.globalData.userInfo) {
        wx.request({
          url: app.globalData.url + '/admin/request/',
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
                mask:true
              })
            } else {
              console.log(res);
              if (res.data.code == 102) {
                wx.hideLoading();
                wx.showToast({
                  title: '请勿重复申请',
                  icon: 'error',
                  duration: 1000,
                  mask:true
                })
              } else {
                wx.hideLoading();
                wx.showToast({
                  title: '提交申请失败',
                  icon: 'error',
                  duration: 1500,
                })
              }
            }
          },
          fail: (res) => {
            wx.hideLoading();
            util.show_error(res)
          }
        })
      } else {
        wx.hideLoading();
        wx.showToast({
          title: '请先绑定信息',
          icon: 'error',
          duration: 1500,
          mask:true
        });
      }
    }
  },
  //反馈建议
  advice() {
    if (app.globalData.login == false) {
      wx.showToast({
        title: '未成功登录',
        icon: 'error',
        duration: 1500,
        mask:true
      })
    } else {
      wx.navigateTo({
        url: '../advice/advice?admin=0',
      })
    }
  },
  //扫描二维码
  async scanQR() {
    if (app.globalData.login == false) {
      wx.showToast({
        title: '未成功登录',
        icon: 'error',
        duration: 1500,
        mask:true
      })
    } else {
      wx.scanCode({
        onlyFromCamera: true,
        scanType: ['qrCode'],
        success: res => {
          wx.login().then(loginRes => {
            wx.showModal({
              title: '登录网页端',
              content: '是否确认登录？',
              success(modelRes) {
                if (modelRes.confirm) {
                  wx.request({
                    url: `${app.globalData.webBackendUrl}/weblogin`,
                    method: 'POST',
                    dataType: 'json',
                    data: {
                      requestId: res.result,
                      credential: loginRes.code
                    },
                    success: ({
                      data
                    }) => {
                      if (data.code === 0) {
                        wx.showToast({
                          title: '登录成功',
                          icon: 'success',
                          duration: 1500,
                          mask:true
                        });
                      } else {
                        wx.showToast({
                          title: data.msg,
                          icon: 'error',
                          duration: 1500,
                          mask:true
                        });
                      }
                    },
                    fail: (res) => {
                     console.log(res)
                      wx.showToast({
                        title: '拉取信息失败',
                        icon: 'error',
                        duration: 1500,
                        mask:true
                      });
                    }
                  });
                }
              }
            });
          });
        }
      });
    }
  },
  //退出登录
  quit() {
    if (app.globalData.login) {
      wx.showModal({
        title: '提示',
        content: '确认要退出登录吗?',
        success: (res) => {
          if (res.confirm) {
            console.log('用户点击确定')
            wx.clearStorageSync()
            app.globalData.login = false
            app.globalData.isadmin = false
            app.globalData.userInfo = false
            this.onShow()
            wx.showToast({
              title: '请退出后重新登录',
              icon: 'none',
              duration: 1500,
              mask:true
            })
          } else if (res.cancel) {
            console.log('用户点击取消')
          }
        }
      })
    } else {
      wx.showToast({
        title: '请退出后重新登录',
        icon: 'none',
        duration: 1500,
        mask:true
      })
    }
  },
  //隐藏测试界面
  hide_test(){
    this.setData({
      index:this.data.index+1
    })
    if(this.data.index==8)
    {
      this.setData({
        index:0
      })
      wx.navigateTo({
        url: '../hide/hide',
      })
    }
  },
});