// appointment.js
const app = getApp()

Page({
  data: {
    sum: 0,
    page: 0,
    items: [],

    complete: false,

    servers: '',
    imgUrls: [{
        pic: '/image/green.png',
        url: '../advice/advice?admin=0'
      },
      {
        pic: '/image/blue.png',
        url: '../advice/advice?admin=0'
      },
      {
        pic: '/image/orange.png',
        url: '../advice/advice?admin=0'
      }
    ],
  },
  //触底加载更多信息
  onReachBottom() {
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    if (this.data.page * 20 < this.data.sum) {
      wx.request({
        url: app.globalData.url + '/item/?p=<page>',
        data: {
          p: this.data.page + 1
        },
        method: 'GET',
        success: (res) => {
          if (res.data.code == 0) {
            this.setData({
              page: this.data.page + 1,
              sum: res.data['item-count'],
              items: this.data.items.concat(res.data.items)
            })
            wx.hideLoading();
          } else {
            console.log(res)
            wx.hideLoading();
            wx.showToast({
              title: '连接错误',
              icon: 'error',
              duration: 1500
            })
          }
        },
        fail: (res) => {
          console.log(res)
          wx.hideLoading();
          wx.showToast({
            title: '连接失败',
            icon: 'error',
            duration: 1500
          });
          stop = true;
        }
      });
    } else {
      wx.hideLoading();
      wx.showToast({
        title: '没有更多了',
        icon: 'none',
        duration: 1500
      });
    }
  },
  //轮播图链接
  goforurl(e) {
    if (app.globalData.login == false) {
      wx.showToast({
        title: '未成功登录',
        icon: 'error',
        duration: 1000
      });
    } else {
      var i = e.currentTarget.dataset['value']
      console.log(i)
      wx.navigateTo({
        url: this.data.imgUrls[i].url,
      })
    }
  },
  //初始化
  onLoad() {
    wx.setNavigationBarTitle({
      title: '预约物品'
    })
    this.refresh();
  },
  onTabItemTap() {
    this.refresh();
  },
  onPullDownRefresh() {
    this.refresh();
  },
  refresh() {
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    if (!this.data.complete) {
      let that = this
      app.getUserInfo().then(function () {
        that.setData({
          complete: true
        })
        that.getitem()
      }).catch(function (res) {
        console.log(res)
        wx.hideLoading()
        wx.showToast({
          title: '读取信息失败',
          icon: 'error',
          duration: 1500
        })
      })
    } else {
      wx.showLoading({
        mask: true,
        title: '加载中',
      })
      this.getitem()
    }
  },
  //读取物品信息
  getitem() {
    this.setData({
      items: []
    })
    wx.request({
      url: app.globalData.url + '/item/?p=<page>',
      data: {
        p: 1
      },
      method: 'GET',
      success: (res) => {
        if (res.data.code == 0) {
          this.setData({
            page: 1,
            sum: res.data['item-count'],
            items: this.data.items.concat(res.data.items)
          })
          wx.hideLoading();
        } else {
          console.log(res)
          wx.hideLoading();
          wx.showToast({
            title: '连接错误',
            icon: 'error',
            duration: 1500
          })
        }
      },
      fail: (res) => {
        console.log(res)
        wx.hideLoading();
        wx.showToast({
          title: '连接失败',
          icon: 'error',
          duration: 1500
        });
      }
    });
  },
  //展示物品信息
  chooseMe(e) {
    let value = e.currentTarget.dataset.value
    if (app.globalData.login == false) {
      wx.showToast({
        title: '未成功登录',
        icon: 'error',
        duration: 1000
      });
    } else if (app.globalData.userInfo) {
      wx.navigateTo({
        url: 'admit/admit?id=' + this.data.items[value].id
      })
    } else {
      wx.showToast({
        title: '未绑定信息',
        icon: 'error',
        duration: 1000
      });
      setTimeout(function () {
        wx.navigateTo({
          url: '../bind/bind'
        })
      }, 1000)
    }
  },
  //展示放大后图片
  preview(e) {
    wx.previewImage({
      urls: [e.currentTarget.dataset['url']],
    })
  },
  //测试专用
  great() {
    if (app.globalData.userInfo)
      app.globalData.userInfo = false
    else
      app.globalData.userInfo = true
  },
  better() {
    if (app.globalData.login)
      app.globalData.login = false
    else
      app.globalData.login = true
  },
  evolve() {
    if (app.globalData.isadmin)
      app.globalData.isadmin = false
    else
      app.globalData.isadmin = true
  },
})