// pages/admin/admin.js
const app = getApp()
Page({
  data: {
    activeTab: 0,
    sum: 0,
    page: 1,
    rsv_list: [],
    item_list: [{
      name: "RTX3060",
      id: 1001,
      available: true,
      'brief-intro': '为降低温度及我觉得大姐大街我i大家',
      thumbnail: "../../icon/add.png"
    }],
    be_list: [],
    admin_list: [],
  },
  onLoad: function () {
    wx.setNavigationBarTitle({
      title: '系统管理'
    })
  },
  onShow: function () {
    this.refresh(this.data.activeTab)
  },
  refresh: function (t) {
    if (t == 0)
      this.refresh_rsv();
    else if (t == 1)
      this.refresh_equip();
    else
      this.refresh_admin();
  },
  //处理不同界面的函数
  refresh_rsv: function () {

  },
  refresh_equip: function () {
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    wx.request({
      url: app.globalData.url + '/item?p=<page>/',
      data: {
        p: 1
      },
      method: 'GET',
      success: (res) => {
        if (res.data.code == 0) {
          this.setData({
            page: 2,
            sum: res.data['item-count'],
            item_list: this.data.item_list.concat(res.data.items)
          })
          wx.hideLoading();
        } else {
          console.log(res.data.code, res.data.errmsg)
          wx.hideLoading();
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
    });
  },
  refresh_admin: function () {
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
            admin_list: res.data.list
          });
          wx.hideLoading()
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
        wx.hideLoading()
        wx.showToast({
          title: '连接失败',
          icon: 'error',
          duration: 1500
        })
      }
    })
  },
  onReachBottom: function () {
    if (app.globalData.activeTab == 1) {
      wx.showLoading({
        mask: true,
        title: '加载中',
      })
      if (this.data.page * 20 < this.data.sum) {
        wx.request({
          url: app.globalData.url + '/item?p=<page>/',
          data: {
            p: this.data.page
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
              console.log(res.data.code, res.data.errmsg)
              wx.hideLoading();
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
    }
  },
  onPullDownRefresh: function () {
    this.refresh(this.data.activeTab);
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
    this.refresh(this.data.activeTab)
  },
  //审批预约

  //管理设备
  addequip(e) {
    wx.navigateTo({
      url: '../equip/equip?id=0',
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
      success: function (res) {
        if (res.confirm) {
          wx.showLoading({
            mask: true,
            title: '提交中',
          })
          wx.request({
            url: app.globalData.url + '/item/<item-id>',
            header: {
              'content-type': 'application/json; charset=utf-8',
              'cookie': wx.getStorageSync('cookie')
            },
            method: 'DELETE',
            data: {
              'item-id': value
            },
            success: (res) => {
              if (res.data.code == 0) {
                wx.hideLoading();
                wx.showToast({
                  title: '删除成功',
                  icon: 'success',
                  duration: 1500
                });
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
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },
  //调整管理员
  req: function (id, p) {
    wx.showLoading({
      mask: true,
      title: '提交中',
    })
    wx.request({
      url: app.globalData.url + '/admin/request/' + id,
      method: 'POST',
      data: {
        p: p,
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
        } else {
          console.log(res.data.code, res.data.errmsg)
          wx.hideLoading();
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
  },
  refuse(e) {
    let value = e.currentTarget.dataset.value
    wx.showModal({
      title: '提示',
      content: '确认要拒绝管理员申请?',
      success: function (res) {
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
      success: function (res) {
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