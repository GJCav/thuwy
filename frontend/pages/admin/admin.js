// pages/admin/admin.js
const app = getApp()
const util = require('../../utils/util.js')
Page({
  data: {
    activeTab: 0,
    sum: 0,
    page: 1,
    p1: 0,
    p2: 0,
    rsv_list1: [],
    rsv_list2: [],
    item_list: [],
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
  //封装信息读取函数
  waiting(page) { //获取待审批预约
    let that=this
    return new Promise(function (resolve, reject) {
      wx.showLoading({
        mask: true,
        title: '加载中',
      })
      var wait_rsvs = [];
      wx.request({
        url: app.globalData.url + '/reservation/?state=1&p='+page,
        header: {
          'content-type': 'application/json; charset=utf-8',
          'cookie': wx.getStorageSync('cookie')
        },
        method: 'GET',
        success: (res) => {
          if (res.data.code == 0) {
            wait_rsvs = res.data.rsvs
            that.setData({
              p1 : res.data.page
            })
            console.log(wait_rsvs);
            //读取设备名称                        
            for (let i in wait_rsvs) {
              let item = wait_rsvs[i]
              util.the_name(item['item-id']).then(function (value) {
                item.item_name = value
              }).catch(function (res) {
                reject(res)
              })
            }
            resolve(wait_rsvs)
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
    let that=this
    return new Promise(function (resolve, reject) {
      wx.showLoading({
        mask: true,
        title: '加载中',
      })
      var go_rsvs = []
      wx.request({
        url: app.globalData.url + '/reservation/?state=2&p='+page,
        header: {
          'content-type': 'application/json; charset=utf-8',
          'cookie': wx.getStorageSync('cookie')
        },
        method: 'GET',
        success: (res) => {
          if (res.data.code == 0) {
            go_rsvs = res.data.rsvs
            that.setData({
              p2 : res.data.page
            })
            console.log(go_rsvs);
            //读取设备名称                        
            for (let i in go_rsvs) {
              let item = go_rsvs[i]
              util.the_name(item['item-id']).then(function (value) {
                item.name = value
              }).catch(function (res) {
                reject(res)
              })
            }
            resolve(go_rsvs)
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
  refresh_rsv: function () {
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    let that = this
    that.waiting(1).then(function (res1) { //读取待审批的预约
      that.going(1).then(function (res2) { //读取进行中的预约
        that.setData({   
          rsv_list1: res1,
          rsv_list2: res2,
        })
        wx.hideLoading()
      }).catch(function(res) {
          console.log(res.data.code,res.data.errmsg)
          wx.hideLoading();
          wx.showToast({
              title: '连接失败',
              icon: 'error',
              duration: 1500
          });
      })
    }).catch(function (res) {
      console.log(res.data.code,res.data.errmsg)
      wx.hideLoading();
      wx.showToast({
          title: '连接失败',
          icon: 'error',
          duration: 1500
      });
    })
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
            page: 1,
            sum: res.data['item-count'],
            item_list: res.data.items
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
            be_list: res.data.list
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
    if (this.data.activeTab == 1) {
      wx.showLoading({
        mask: true,
        title: '加载中',
      })
      if (this.data.page * 20 < this.data.sum) {
        wx.request({
          url: app.globalData.url + '/item?p=<page>/',
          data: {
            p: this.data.page+1
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
  //加载更多信息
  loadwait(){
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    let that=this
    this.waiting(this.data.p1+1).then(function(res){
      if(res=='')
      {
        wx.hideLoading()
        wx.showToast({
          title: '没有更多了',
          icon: 'none',
          duration: 1500
        });
      } else{
        that.setData({
          rsv_list1:that.data.rsv_list1.concat(res)
        })
        wx.hideLoading()
      }
    }).catch(function(res){
      console.log(res)
      wx.hideLoading();
      wx.showToast({
        title: '连接失败',
        icon: 'error',
        duration: 1500
      });
    })
  },
  loadgo(){
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    let that=this
    this.going(this.data.p2+1).then(function(res){
      if(res=='')
      {
        wx.hideLoading()
        wx.showToast({
          title: '没有更多了',
          icon: 'none',
          duration: 1500
        });
      } else{
        that.setData({
          rsv_list2:that.data.rsv_list2.concat(res)
        })
        wx.hideLoading()
      }
    }).catch(function(res){
      console.log(res.data.code, res.data.errmsg)
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
    var name = e.currentTarget.dataset['name']
    var who = e.currentTarget.dataset['value']
    wx.navigateTo({
      url: '../reservation/reservation?rsvid=' + rsvid + '&who=' + who + '&name=' + name,
    })
  },
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
      success: (res) => {
        if (res.confirm) {
          wx.showLoading({
            mask: true,
            title: '提交中',
          })
          wx.request({
            url: app.globalData.url + '/item/' + value,
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