// appointment.js
const app = getApp()
const util = require('../../utils/util.js') 
Page({
  data: {
    sum: 0,
    page: 0,
    items: [],

    cur_group:'',
    item_group:[],

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
            wx.hideLoading();
            util.show_error(res)
          }
        },
        fail: (res) => {
          wx.hideLoading();
          util.show_error(res)

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
        duration: 1000,
        mask:true
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
    this.setData({
      item_group:app.globalData.item_group,
      cur_group:app.globalData.item_group[0]
    })
    this.refresh();
  },
  onTabItemTap() {
    this.refresh();
  },
  onPullDownRefresh() {
    this.refresh();
    wx.stopPullDownRefresh();
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
        //管理员直接跳转到管理界面
        if(app.globalData.isadmin)
        {
          wx.navigateTo({
            url: '../admin/admin',
          })
        }
      }).catch(function (res) {
        wx.hideLoading()
        util.show_error(res)
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
    const the_group=this.data.cur_group
    wx.request({
      url: app.globalData.url + '/item/?p=1'+(the_group=='全部物品'?'':('&group='+(the_group=='其他物品'?'无分组':the_group))),
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
          wx.hideLoading();
          util.show_error(res)
        }
      },
      fail: (res) => {
        wx.hideLoading();
        util.show_error(res)
      }
    });
  },
  //展示物品信息
  chooseMe(e) {
    let value = e.currentTarget.dataset.value
    if (app.globalData.login == false) {
      wx.showToast({
        title: '未成功登录',
        mask:true,
        duration: 1000
      });
    } else if (app.globalData.userInfo) {
      wx.navigateTo({
        url: 'admit/admit?id=' + this.data.items[value].id
      })
    } else {
      wx.showToast({
        title: '未绑定信息',
        mask:true,
        duration: 1000
      });
      setTimeout(function () {
        wx.navigateTo({
          url: '../bind/bind'
        })
      }, 1000)
    }
  },
  //选择预约组别
  choose_group(e){
    this.setData({
      cur_group:this.data.item_group[e.detail.value]
    })
    this.refresh()
  },
  //展示放大后图片
  preview(e) {
    wx.previewImage({
      urls: [e.currentTarget.dataset['url']],
    })
  },
})