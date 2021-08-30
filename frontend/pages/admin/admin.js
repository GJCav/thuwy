// pages/admin/admin.js
const app = getApp()
//备用
// const util = require('../../utils/util.js') 
Page({
  data: {
    activeTab: 0,
    sum: 0, //物品总数
    page: 1, //物品页码
    p1: 0,
    p2: 0,
    p3: 0,
    p4: 0,
    pan1: false,
    pan2: false,
    pan3: false,
    pan4: false,
    rsv_list1: [], //预约列表
    rsv_list2: [], //进行中预约列表
    advice_list: [], //建议列表
    checked_list: [], //已审核建议列表
    item_list: [], //物品列表
    be_list: [], //管理员申请列表
    admin_list: [], //管理员列表
  },
  onLoad: function () {
    wx.setNavigationBarTitle({
      title: '系统管理'
    })
    this.refresh()
  },
  refresh: function () {
    var t = this.data.activeTab
    if (t == 0)
      this.refresh_rsv();
    else if (t == 1)
      this.refresh_equip();
    else if (t == 2)
      this.refresh_advice();
    else
      this.refresh_admin();
  },
  //封装信息读取函数
  waiting(page) { //获取待审批预约
    let that = this
    return new Promise(function (resolve, reject) {
      wx.showLoading({
        mask: true,
        title: '加载中',
      })
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
            if (page > 1 && wait_rsvs == '') {
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
      wx.showLoading({
        mask: true,
        title: '加载中',
      })
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
            if (page > 1 && go_rsvs == '') {
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
  advice(page) {
    let that = this
    return new Promise(function (resolve, reject) {
      wx.showLoading({
        mask: true,
        title: '加载中',
      })
      wx.request({
        url: app.globalData.url + '/advice/?state=<state>&p=<page>',
        method: 'GET',
        header: {
          'content-type': 'application/json; charset=utf-8',
          'cookie': wx.getStorageSync('cookie')
        },
        data: {
          state: 1,
          p: page
        },
        success: (res) => {
          if (res.data.code == 0) {
            let advice = res.data.advice
            that.setData({
              p3: res.data.page,
            })
            if (page > 1 && advice == '') {
              that.setData({
                pan3: true
              })
            }
            that.setData({
              advice_list: that.data.advice_list.concat(advice)
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
  checked(page) {
    let that = this
    return new Promise(function (resolve, reject) {
      wx.showLoading({
        mask: true,
        title: '加载中',
      })
      wx.request({
        url: app.globalData.url + '/advice/?state=<state>&p=<page>',
        method: 'GET',
        header: {
          'content-type': 'application/json; charset=utf-8',
          'cookie': wx.getStorageSync('cookie')
        },
        data: {
          state: 2,
          p: page
        },
        success: (res) => {
          if (res.data.code == 0) {
            let advice = res.data.advice
            that.setData({
              p4: res.data.page,
            })
            if (page > 1 && advice == '') {
              that.setData({
                pan4: true
              })
            }
            that.setData({
              checked_list: that.data.checked_list.concat(advice)
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
        console.log(res)
        wx.hideLoading();
        wx.showToast({
          title: '连接失败',
          icon: 'error',
          duration: 1500
        });
      })
    }).catch(function (res) {
      console.log(res)
      wx.hideLoading();
      wx.showToast({
        title: '连接失败',
        icon: 'error',
        duration: 1500
      });
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
  refresh_advice() {
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    let that=this
    that.setData({
      advice_list: [],
      checked_list: []
    })
    that.advice(1).then(function () { //读取未审阅的建议
      that.checked(1).then(function () { //读取已审阅的建议
        wx.hideLoading()
      }).catch(function (res) {
        console.log(res)
        wx.hideLoading();
        wx.showToast({
          title: '连接失败',
          icon: 'error',
          duration: 1500
        });
      })
    }).catch(function (res) {
      console.log(res)
      wx.hideLoading();
      wx.showToast({
        title: '连接失败',
        icon: 'error',
        duration: 1500
      });
    })
  },
  refresh_admin() {
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    wx.request({
      url: app.globalData.url + '/admin/request/',
      method: 'GET',
      header: {
        'content-type': 'application/json; charset=utf-8',
        'cookie': wx.getStorageSync('cookie')
      },
      success: (res) => {
        if (res.data.code == 0) {
          this.setData({
            be_list: res.data.list
          });
          wx.hideLoading()
        } else {
          console.log(res)
          wx.hideLoading()
          wx.showToast({
            title: '连接错误',
            icon: 'error',
            duration: 1500
          })
        }
      },
      fail: (res) => {
        console.log(res)
        wx.hideLoading()
        wx.showToast({
          title: '连接失败',
          icon: 'error',
          duration: 1500
        })
      }
    })
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
      case 3:
        this.setData({
          activeTab: 3
        });
        break;
    }
    this.refresh()
  },
  //加载更多预约信息
  loadwait() {
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    let that = this
    this.setData({
      pan1: false
    })
    this.waiting(this.data.p1 + 1).then(function () {
      if (that.data.pan1 == false) {
        wx.hideLoading()
        wx.showToast({
          title: '没有更多了',
          icon: 'none',
          duration: 1500
        })
      }
    }).catch(function (res) {
      console.log(res)
      wx.hideLoading();
      wx.showToast({
        title: '连接失败',
        icon: 'error',
        duration: 1500
      });
    })
  },
  loadgo() {
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    let that = this
    this.going(this.data.p2 + 1).then(function () {
      if (that.data.pan1 == false) {
        wx.hideLoading()
        wx.showToast({
          title: '没有更多了',
          icon: 'none',
          duration: 1500
        })
      }
    }).catch(function (res) {
      console.log(res)
      wx.hideLoading();
      wx.showToast({
        title: '连接失败',
        icon: 'error',
        duration: 1500
      });
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
                console.log(res)
                wx.hideLoading()
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
          })
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },
  //加载更多建议信息
  loadadvice() {
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    let that = this
    this.setData({
      pan3: false
    })
    this.waiting(this.data.p3 + 1).then(function () {
      if (that.data.pan3 == false) {
        wx.hideLoading()
        wx.showToast({
          title: '没有更多了',
          icon: 'none',
          duration: 1500
        })
      }
    }).catch(function (res) {
      console.log(res)
      wx.hideLoading();
      wx.showToast({
        title: '连接失败',
        icon: 'error',
        duration: 1500
      });
    })
  },
  loadchecked() {
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    let that = this
    this.setData({
      pan4: false
    })
    this.waiting(this.data.p4 + 1).then(function () {
      if (that.data.pan4 == false) {
        wx.hideLoading()
        wx.showToast({
          title: '没有更多了',
          icon: 'none',
          duration: 1500
        })
      }
    }).catch(function (res) {
      console.log(res)
      wx.hideLoading();
      wx.showToast({
        title: '连接失败',
        icon: 'error',
        duration: 1500
      });
    })
  },
  //意见反馈
  showadvice(e) {
    var id = e.currentTarget.dataset['id']
    wx.navigateTo({
      url: '../advice/advice?id=' + id,
    })
  },
  //调整管理员
  req: function (id, p) {
    wx.showLoading({
      mask: true,
      title: '提交中',
    })
    wx.request({
      url: app.globalData.url + '/admin/request/' + id + '/',
      method: 'POST',
      header: {
        'content-type': 'application/json; charset=utf-8',
        'cookie': wx.getStorageSync('cookie')
      },
      data: {
        pass: p,
        reason: ""
      },
      success: (res) => {
        if (res.data.code == 0) {
          wx.hideLoading();
          wx.showToast({
            title: '审批成功',
            icon: 'success',
            duration: 1500
          })
          this.refresh_admin();
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
    })
  },
  refuse(e) {
    let value = e.currentTarget.dataset.value
    wx.showModal({
      title: '提示',
      content: '确认要拒绝管理员申请?',
      success: (res) => {
        if (res.confirm) {
          console.log('用户点击确定')
          this.req(value, 0)
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },
  approve(e) {
    let value = e.currentTarget.dataset.value
    wx.showModal({
      title: '提示',
      content: '确认要同意管理员申请?',
      success: (res) => {
        if (res.confirm) {
          console.log('用户点击确定')
          this.req(value, 1)
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },
  fired(e) {
    wx.showToast({
      title: '功能尚未开通',
      icon: 'error',
      duration: 1500
    });
  }
})