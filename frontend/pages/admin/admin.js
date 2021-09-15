// pages/admin/admin.js
const app = getApp()
const util = require('../../utils/util.js') 
Page({
  data: {
    activeTab: 0,
    sum: 0, //物品总数
    page: 1, //物品页码
    p1: 0,
    p2: 0,
    pan1: false,
    pan2: false,
    rsv_list1: [], //预约列表
    rsv_list2: [], //进行中预约列表
    item_list: [], //物品列表
    line: 0,
    else: [{
        name: '意见反馈',
        go_url: '../advice/advice?admin=1',
        pic_url: '../../image/advice.png'
      },
      {
        name: '权限管理',
        go_url: '../administrator/administrator',
        pic_url: '../../image/power.png'
      },
      {
        name: '宣传栏调整',
        go_url: '../carousel/carousel',
        pic_url: '../../image/carousel.png'
      }
    ]
  },
  onLoad: function () {
    wx.setNavigationBarTitle({
      title: '系统管理'
    })
    this.refresh()
    this.setData({
      line: parseInt((this.data.else.length - 1) / 3) + 1
    })
  },
  refresh: function () {
    var t = this.data.activeTab
    if (t == 0)
      this.refresh_rsv();
    else if (t == 1)
      this.refresh_equip();
  },
  //封装信息读取函数
  waiting(page) { //获取待审批预约
    let that = this
    return new Promise(function (resolve, reject) {
      wx.request({
        url: app.globalData.url + '/reservation/?state=1&p=' + page,
        header: {
          'content-type': 'application/json; charset=utf-8',
          'cookie': wx.getStorageSync('cookie')
        },
        method: 'GET',
        success: (res) => {
          if (res.data.code == 0) {
            let wait_rsvs = res.data.rsvs
            that.setData({
              p1: res.data.page,
            })
            if (page > 1 && wait_rsvs.length == 0) {
              that.setData({
                pan2: true
              })
            }
            that.setData({
              rsv_list1: that.data.rsv_list1.concat(wait_rsvs)
            })
            resolve()
          } else {
            reject(res)
          }
        },
        fail: (res) => {
          reject(res)
        }
      })
    })
  },
  going(page) { //获取进行中预约
    let that = this
    return new Promise(function (resolve, reject) {
      wx.request({
        url: app.globalData.url + '/reservation/?state=2&p=' + page,
        header: {
          'content-type': 'application/json; charset=utf-8',
          'cookie': wx.getStorageSync('cookie')
        },
        method: 'GET',
        success: (res) => {
          if (res.data.code == 0) {
            let go_rsvs = res.data.rsvs
            that.setData({
              p2: res.data.page,
            })
            if (page > 1 && go_rsvs.length == 0) {
              that.setData({
                pan2: true
              })
            }
            that.setData({
              rsv_list2: that.data.rsv_list2.concat(go_rsvs)
            })
            resolve()
          } else {
            reject(res)
          }
        },
        fail: (res) => {
          reject(res)
        }
      })
    })
  },
  //处理不同界面的函数
  refresh_rsv() {
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    let that = this
    that.setData({
      rsv_list1: [],
      rsv_list2: []
    })
    that.waiting(1).then(function () { //读取待审批的预约
      that.going(1).then(function () { //读取进行中的预约
        wx.hideLoading()
      }).catch(function (res) {
        wx.hideLoading();
        util.show_error(res)
      })
    }).catch(function (res) {
      wx.hideLoading();
      util.show_error(res)
    })
  },
  refresh_equip() {
    wx.showLoading({
      mask: true,
      title: '加载中',
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
            item_list: res.data.items
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
  //刷到底部刷新
  onReachBottom() {
    if (this.data.activeTab == 1) {
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
    }
  },
  onPullDownRefresh() {
    this.refresh();
    wx.stopPullDownRefresh();
  },
  switchTab(e) {
    switch (e.detail.index) {
      case 0:
        this.setData({
          activeTab: 0,
        });
        break;
      case 1:
        this.setData({
          activeTab: 1
        });
        break;
      case 2:
        this.setData({
          activeTab: 2
        });
        break;
    }
    this.refresh()
  },
  //加载更多预约信息
  load_wait() {
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    let that = this
    this.setData({
      pan1: false
    })
    this.waiting(this.data.p1 + 1).then(function () {
      wx.hideLoading()
      if (that.data.pan1) {
        wx.showToast({
          title: '没有更多了',
          icon: 'none',
          duration: 1500
        })
      }
    }).catch(function (res) {
      wx.hideLoading();
      util.show_error(res)
    })
  },
  load_go() {
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    let that = this
    this.going(this.data.p2 + 1).then(function () {
      wx.hideLoading()
      if (that.data.pan2) {
        wx.showToast({
          title: '没有更多了',
          icon: 'none',
          duration: 1500
        })
      }
    }).catch(function (res) {
      wx.hideLoading();
      util.show_error(res)
    })
  },
  //审批预约
  showdetail(e) {
    var rsvid = e.currentTarget.dataset['id']
    var who = e.currentTarget.dataset['value']
    wx.navigateTo({
      url: '../reservation/reservation?rsvid=' + rsvid + '&who=' + who,
    })
  },
  //管理设备
  preview(e) { //展示放大后图片
    wx.previewImage({
      urls: [e.currentTarget.dataset['url']],
    })
  },
  addequip(e) {
    wx.navigateTo({
      url: '../equip/equip?id=0'
    })
  },
  modify(e) {
    let value = e.currentTarget.dataset.value
    wx.navigateTo({
      url: '../equip/equip?id=' + value,
    })
  },
  del(e) {
    let value = e.currentTarget.dataset.value
    wx.showModal({
      title: '提示',
      content: '确认要删除物品?',
      success: (res) => {
        if (res.confirm) {
          wx.showLoading({
            mask: true,
            title: '提交中',
          })
          wx.request({
            url: app.globalData.url + '/item/' + value + '/',
            header: {
              'content-type': 'application/json; charset=utf-8',
              'cookie': wx.getStorageSync('cookie')
            },
            method: 'DELETE',
            success: (res) => {
              if (res.data.code == 0) {
                wx.hideLoading();
                wx.showToast({
                  title: '删除成功',
                  icon: 'success',
                  duration: 1500
                });
                this.refresh_equip();
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
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },
  //更多功能
  link_start(e) {
    wx.navigateTo({
      url: e.currentTarget.dataset['value'],
    })
  },
})