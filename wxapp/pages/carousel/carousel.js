// pages/carousel/carousel.js
Page({
    data: {

    },
    onLoad: function (options) {
        wx.setNavigationBarTitle({
            title: '宣传栏调整'
          })
        wx.showToast({
            mask: true,
            title: '该功能暂未开通',
            icon: 'error',
            duration: 1500
          })
          setTimeout(function () {
            wx.navigateBack({
              delta: 1
            })
          }, 1500)
    },
})