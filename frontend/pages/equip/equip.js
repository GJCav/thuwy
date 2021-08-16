// pages/equip/equip.js
// 获取应用实例
const app = getApp()

Page({
  data: {
    item_id: 0,
    name: '',
    available: true,
    brief_intro: '',
    md_intro: '',
    rsv_method: 0,
    thumbnail: '',
    havepic:false,
    methods: [{
      value: 1,
      checked: false,
      can: true,
      name: '固定时间段预约'
    }, {
      value: 2,
      checked: false,
      can: false,
      name: '自由时间段预约(未支持)'
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
  inputcan: function (e) {
    this.data.available = e.detail.value
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
  choosepic:function(e){
    wx.chooseImage({
      count: 1,
      sourceType: e.currentTarget.dataset.way,
      success:(res)=> {
        this.setData({
          thumbnail:res.tempFilePaths[0],
          havepic:true
        });
      },
      fail: (res)=>{
        wx.showToast({
            title: '读取失败',
            icon: 'error'
          })
          this.setData({
            thumbnail:'',
            havepic:false
          });
        },
    })
  },
  onLoad: function (options) {
    if (options.id != 0) {
      wx.setNavigationBarTitle({
        title: '修改设备'
      })
      wx.showLoading({
        mask: true,
        title: '加载中',
      })
      this.setData({
        item_id: options.id
      })
      wx.request({
        url: app.globalData.url + '/item/' + this.data.item_id,
        method: 'GET',
        success: (res) => {
          let those = res.data
          console.log(those)
          if (those.code == 0) {
            this.setData({
              name: those.item.name,
              brief_intro: those.item['brief-intro'],
              md_intro: those.item['md-intro'],
              rsv_method: those.item['rsv-method'],
              thumbnail: those.item.thumbnail,
              available: those.item.available
            })
            let that = this.data
            if (that.rsv_method % 2 == 1) {
              this.setData({
                'methods[0].checked': true
              })
            }
            if (parseInt(that.rsv_method / 2) % 2 == 1) {
              this.setData({
                'methods[1].checked': true
              })
            }
            wx.hideLoading()
          } else {
            console.log(res.data.code, res.data.errmsg)
            wx.hideLoading()
            wx.showToast({
              mask: true,
              title: '连接错误',
              icon: 'error',
              duration: 1500
            })
            setTimeout(function () {
              wx.navigateBack({
                delta: 1
              })
            }, 1500)
          }
        },
        fail: (res) => {
          console.log(res.data.code, res.data.errmsg)
          wx.hideLoading()
          wx.showToast({
            mask: true,
            title: '连接失败',
            icon: 'error',
            duration: 1500
          })
          setTimeout(function () {
            wx.navigateBack({
              delta: 1
            })
          }, 1500)
        }
      })
    } else {
      wx.setNavigationBarTitle({
        title: '添加设备'
      })
    }
  },
  onShow() {
    wx.enableAlertBeforeUnload({
      message: '您确定要离开此页面吗？已经填写的信息将会丢失',
    })
  },
  addit() {
    let that = this.data
    if (that.mame == '' || that.rsv_method == 0 || that.brief_intro == '' || that.thumbnail == '') {
      wx.showToast({
        title: '信息未填写完整',
        icon: 'error',
        duration: 1500
      })
    } else if (that.item_id == 0) {
      wx.showLoading({
        title: '提交中',
        mask: true
      })
      //上传图片
      // wx.uploadFile({
      //   filePath: this.data.thumbnail,
      //   name: 'name',
      //   url: 'url',
      // })
      wx.request({
        header: {
          'content-type': 'application/json; charset=utf-8',
          'cookie': wx.getStorageSync('cookie')
        },
        url: app.globalData.url + '/item/',
        method: "POST",
        data: {
          name: that.name,
          'brief-intro': that.brief_intro,
          'md-intro': that.md_intro,
          thumbnail: that.thumbnail,
          'rsv-method': that.rsv_method
        },
        success: (res) => {
          if (res.data.code == 0) {
            wx.hideLoading();
            wx.showToast({
              mask: true,
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
    } else {
      wx.showLoading({
        title: '提交中',
        mask: true
      })
      wx.request({
        header: {
          'content-type': 'application/json; charset=utf-8',
          'cookie': wx.getStorageSync('cookie')
        },
        url: app.globalData.url + '/item/' + that.item_id,
        method: "POST",
        data: {
          name: that.name,
          'brief-intro': that.brief_intro,
          'md-intro': that.md_intro,
          thumbnail: that.thumbnail,
          'rsv-method': that.rsv_method,
          available: that.available
        },
        success: (res) => {
          if (res.data.code == 0) {
            wx.hideLoading();
            wx.showToast({
              mask: true,
              title: '修改成功',
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
  }
})