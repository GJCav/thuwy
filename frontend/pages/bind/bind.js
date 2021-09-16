// bind.js
const app = getApp()
const util = require('../../utils/util.js')
Page({
  data: {
    loading: false,
    name: '',
    id: '',
    clz: ''
  },
  onLoad() {
    wx.setNavigationBarTitle({
      title: '绑定信息'
    })
  },
  inputname: function (e) {
    this.setData({
      name: e.detail.value
    });
  },
  inputid: function (e) {
    this.setData({
      id: e.detail.value
    });
  },
  inputclz: function (e) {
    this.setData({
      clz: e.detail.value
    });
  },
  addUser() {
    wx.showLoading({
      mask: true,
      title: '提交中',
    })
    wx.request({
      header: {
        'content-type': 'application/json; charset=utf-8',
        'cookie': wx.getStorageSync('cookie')
      },
      url: app.globalData.url + '/bind/',
      method: "POST",
      data: {
        id: this.data.id,
        name: this.data.name,
        clazz: this.data.clz
      },
      success: (res) => {
        if (res.data.code == 0) {
          wx.hideLoading();
          wx.showToast({
            mask: true,
            title: '绑定成功',
            icon: 'success',
            duration: 1500
          });
          app.globalData.userInfo = true;
          setTimeout(function () {
            wx.navigateBack({
              delta: 1
            })
          }, 1500)
        } else {
          wx.hideLoading()
          util.show_error(res)
        }
      },
      fail: (res) => {
        wx.hideLoading();
        util.show_error(res)
      }
    })
  }
})