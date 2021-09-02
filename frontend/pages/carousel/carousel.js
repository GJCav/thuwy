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

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function () {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function () {

    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function () {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload: function () {

    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function () {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function () {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function () {

    }
})