// bind.js
const app = getApp()
const util = require('../../utils/util.js')
Page({
  data: {
    items: [
      {value: '0', name: '未央学生',checked: true},
      {value: '1', name: '未央管理',checked: false},
    ],
    departs:["未央团工委","党建辅导员","带班辅导员","未央教务"],
    depart:'点击选择',
    loading: false,
    name: '',
    id: '',
    clz: '',
    identity:0
  },
  onLoad() {
    wx.setNavigationBarTitle({
      title: '绑定信息'
    })
  },
  identity(e){
    this.setData({
      clz:'',
      depart:'点击选择',
      identity:parseInt(e.detail.value)
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
  inputdepart:function(e){
    this.setData({
      depart:this.data.departs[e.detail.value],
    });
  },
  addUser() {
    wx.showLoading({
      mask: true,
      title: '提交中',
    })
    console.log((this.data.identity==0?this.data.clz:(this.data.depart=='点击选择'?"":this.data.depart)))
    wx.request({
      header: {
        'content-type': 'application/json; charset=utf-8',
        'Session': wx.getStorageSync('Session')
      },
      url: app.globalData.url + '/bind/',
      method: "POST",
      data: {
        id: this.data.id,
        name: this.data.name,
        clazz: (this.data.identity==0?this.data.clz:(this.data.depart=='点击选择'?"":this.data.depart))
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