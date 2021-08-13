// bind.js
// 获取应用实例
const app = getApp()

Page({
  data: {
    loading: false,
    name: '',
    id: '',
    clz: ''
  },
  onLoad() {
    wx.setNavigationBarTitle({
      title: '绑定信息'
    })
  },
  onShow(){
    wx.enableAlertBeforeUnload({
      message: '您确定要离开此页面吗？已经填写的信息将会丢失',
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
  addUser() {
    if (!(/(^\d+$)/.test(this.data.id))) {
      wx.showToast({
        title: '学号输入有误',
        icon: 'error',
        duration: 1500
      });
    } else if (!(/^未央-.+\d\d$/.test(this.data.clz))) {
      wx.showToast({
        title: '班级输入有误',
        icon: 'error',
        duration: 1500
      });
    } else {
      wx.showLoading({
        mask: true,
        title: '提交中',
      })
      wx.request({
        header: {
          'content-type': 'application/json; charset=utf-8',
          'cookie': wx.getStorageSync('cookie')
        },
        url: app.globalData.url + '/bind/',
        method: "POST",
        data: {
          id: this.data.id,
          name: this.data.name,
          clazz: this.data.clz
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