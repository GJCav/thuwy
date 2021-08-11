// pages/equip/equip.js
// 获取应用实例
const app = getApp()

Page({
  data: {
    item_id: 0,
    name: '',
    brief_intro: '',
    md_intro: '',
    thumbnail: '../../icon/add.png',
    rsv_method: 0,
    methods: [{
      value: 1,
      checked: false,
      name: '固定时间段预约'
    }, {
      value: 2,
      checked: false,
      name: '自由时间段预约'
    }]
  },
  inputname: function (e) {
    this.setData({
      name: e.detail.value
    });
  },
  inputintro: function (e) {
    this.setData({
      brief_intro: e.detail.value
    });
  },
  inputmd: function (e) {
    this.setData({
      md_intro: e.detail.value
    });
  },
  rsvmethod: function (e) {
    let sel = e.detail.value
    var sum = 0
    for (var i = 0; i < sel.length; ++i)
      sum = sum + parseInt(sel[i])
    this.setData({
      rsv_method: sum
    })
    console.log(this.data.rsv_method)
  },
  onLoad: function (options) {
    this.setData({
      item_id: options.id
    })
    wx.setNavigationBarTitle({
      title: '个人管理'
    })
  },
  addit() {
    let that = this.data
    if (that.item_id == 0) {
      if (that.mame == '' || that.rsv_methods == 0 || that.brief_intro == '' || that.thumbnail == '')
        wx.showToast({
          title: '信息未填写完整',
          icon: 'error',
          duration: 1500
        })
      else {
        wx.showLoading({
          title: '提交中',
          mask: true
        })
        wx.request({
          header: {
            'content-type': 'application/json; charset=utf-8',
            'cookie': wx.getStorageSync('cookie')
          },
          url: app.globalData.url + '/item/',
          method: "POST",
          data: {
            item: {
              name: that.name,
              ['brief-intro']: that.brief_intro,
              ['md-intro']: that.md_intro,
              thumbnail: that.thumbnail,
              ['rsv-method']: that.rsv_method
            }
          },
          success: (res) => {
            if (res.data.code == 0) {
              wx.hideLoading();
              wx.showToast({
                title: '添加成功',
                icon: 'success',
                duration: 1500
              });
              setTimeout(function () {
                wx.navigateBack({
                  delta: 1
                })
              }, 1500)
            } else {
              console.log(res.data.code, res.data.errmsg)
              wx.hideLoading()
              wx.showToast({
                title: '连接错误',
                icon: 'error',
                duration: 1500
              })
            }
          },
          fail: (res) => {
            console.log(res.data.code, res.data.errmsg)
            wx.hideLoading();
            wx.showToast({
              title: '连接失败',
              icon: 'error',
              duration: 1500
            });
          }
        })
      }
    } else {

    }
  }
})