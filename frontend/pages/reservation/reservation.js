// pages/reservation/reservation.js
const app = getApp()
Page({
  data: {
    who: 0,
    rsvid: 0,
    rsv_guest: null,
    rsv_detail: {},
    reason: '',
  },
  onLoad: function (options) {
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    this.setData({
      who: options.who,
        //who=0:用户端且已审批
        //who=1:用户端且待审批
        //who=2：管理员端
      rsvid: options.rsvid,
    })
    //获取预约详细信息
    wx.request({
      url: app.globalData.url + '/reservation/' + this.data.rsvid+'/',
      method: 'GET',
      success: (res) => {
        if (res.data.code == 0) {
          this.setData({
            rsv_detail: res.data.rsv,
          })
          console.log(res.data.rsv)
          wx.hideLoading()
        } else {
          console.log(res.data.code, res.data.errmsg);
          wx.hideLoading();
          wx.showToast({
            mask: true,
            title: '连接错误',
            icon: 'error',
            duration: 1500,
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
        wx.hideLoading();
        wx.showToast({
          mask: true,
          title: '连接失败',
          icon: 'error',
          duration: 1500
        });
        setTimeout(function () {
          wx.navigateBack({
            delta: 1
          })
        }, 1500)
      }
    })
  },
  //输入处理
  inputreason(e) {
    this.setData({
      reason: e.detail.value
    });
  },
  //判断是否已经输入
  pan: function () {
    let that = this.data
    if (that.reason == '') {
      wx.showToast({
        title: '未输入审批回复',
        icon: 'error',
        duration: 1500
      });
      return false
    } else
      return true
  },
  //处理情况
  admit() {
    wx.showModal({
      title: '提示',
      content: '确认要批准本次预约?',
      success: (res) => {
        if (this.pan()) {
          if (res.confirm) {
            wx.showLoading({
              mask: true,
              title: '提交中',
            })
            wx.request({
              header: {
                'content-type': 'application/json; charset=utf-8',
                'cookie': wx.getStorageSync('cookie')
              },
              url: app.globalData.url + "/reservation/" + this.data.rsvid+'/',
              method: "POST",
              data: {
                op: 1,
                pass: 1,
                reason: this.data.reason
              },
              success: (res) => {
                if (res.data.code == 0) {
                  wx.hideLoading();
                  wx.showToast({
                    mask: true,
                    title: "审阅成功",
                    icon: 'success',
                    duration: 1500,
                  })
                  setTimeout(function () {
                    wx.navigateBack({
                      delta: 1
                    })
                    let pages = getCurrentPages();
                    let prevPage = pages[pages.length - 2];
                    prevPage.refresh()
                  }, 1500)
                } else {
                  console.log(res.data.code, res.data.errmsg);
                  wx.hideLoading();
                  wx.showToast({
                    title: '审阅失败',
                    icon: 'error',
                    duration: 1500,
                  })
                }
              },
              fail: (res) => {
                console.log(res.data.code, res.data.errmsg);
                wx.hideLoading();
                wx.showToast({
                  title: '连接失败',
                  icon: 'error',
                  duration: 1500
                });
              }
            })
          }
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },
  noway() {
    wx.showModal({
      title: '提示',
      content: '确认要拒绝本次预约?',
      success: (res) => {
        if (res.confirm) {
          if (this.pan()) {
            wx.showLoading({
              mask: true,
              title: '提交中',
            })
            wx.request({
              header: {
                'content-type': 'application/json; charset=utf-8',
                'cookie': wx.getStorageSync('cookie')
              },
              url: app.globalData.url + "/reservation/" + this.data.rsvid+'/',
              method: "POST",
              data: {
                op: 1,
                pass: 0,
                reason: this.data.reason
              },
              success: (res) => {
                if (res.data.code == 0) {
                  wx.hideLoading();
                  wx.showToast({
                    mask: true,
                    title: "审阅成功",
                    icon: 'success',
                    duration: 1500,
                  })
                  setTimeout(function () {
                    wx.navigateBack({
                      delta: 1
                    })
                    let pages = getCurrentPages();
                    let prevPage = pages[pages.length - 2];
                    prevPage.refresh()
                  }, 1500)
                } else {
                  console.log(res.data.code, res.data.errmsg);
                  wx.hideLoading();
                  wx.showToast({
                    title: '审阅失败',
                    icon: 'error',
                    duration: 1500,
                  })
                }
              },
              fail: (res) => {
                console.log(res.data.code, res.data.errmsg);
                wx.hideLoading();
                wx.showToast({
                  title: '连接失败',
                  icon: 'error',
                  duration: 1500
                });
              }
            })
          }
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },
  delete() {
    console.log("delete:" + this.data.rsvid)
    wx.showModal({
      title: '提示',
      content: '确认要取消本次预约?',
      success: (res) => {
        if (res.confirm) {
          wx.showLoading({
            mask: true,
            title: '取消中',
          })
          console.log('用户点击确定')
          wx.request({
            header: {
              'content-type': 'application/json; charset=utf-8',
              'cookie': wx.getStorageSync('cookie')
            },
            url: app.globalData.url + "/reservation/" + this.data.rsvid+'/',
            method: "DELETE",
            success: (res) => {
              if (res.data.code == 0) {
                wx.hideLoading();
                wx.showToast({
                  mask: true,
                  title: "取消成功",
                  icon: 'success',
                  duration: 1500,
                })
                setTimeout(function () {
                  wx.navigateBack({
                    delta: 1
                  })
                  let pages = getCurrentPages();
                  let prevPage = pages[pages.length - 2];
                  prevPage.refresh()
                }, 1500)
              } else {
                console.log(res.data.code, res.data.errmsg);
                wx.hideLoading();
                wx.showToasting({
                  title: '取消失败',
                  icon: 'error',
                  duration: 1500,
                })
              }
            },
            fail: (res) => {
              console.log(res.data.code, res.data.errmsg);
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
  over() {
    console.log("refuse:" + this.data.rsvid)
    wx.showModal({
      title: '提示',
      content: '确认预约物品已归还?',
      success: (res) => {
        if (res.confirm) {
          wx.showLoading({
            mask: true,
            title: '提交中',
          })
          console.log('用户点击确定')
          wx.request({
            header: {
              'content-type': 'application/json; charset=utf-8',
              'cookie': wx.getStorageSync('cookie')
            },
            url: app.globalData.url + "/reservation/" + this.data.rsvid+"/",
            method: "POST",
            data: {
              op: 2,
            },
            success: function (res) {
              if (res.data.code == 0) {
                wx.hideLoading();
                wx.showToast({
                  mask: true,
                  title: "预约结束",
                  icon: 'success',
                  duration: 1500,
                })
                setTimeout(function () {
                  wx.navigateBack({
                    delta: 1
                  })
                  let pages = getCurrentPages();
                  let prevPage = pages[pages.length - 2];
                  prevPage.refresh()
                }, 1500)
              } else {
                console.log(res.data.code, res.data.errmsg);
                wx.hideLoading();
                wx.showToasting({
                  title: '提交失败',
                  icon: 'error',
                  duration: 1500,
                })
              }
            },
            fail: (res) => {
              console.log(res.data.code, res.data.errmsg);
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
  }
})