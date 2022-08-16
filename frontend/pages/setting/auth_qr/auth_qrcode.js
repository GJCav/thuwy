// pages/setting/auth_qr/auth_qrcode.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    scene: ""
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let scene = decodeURIComponent(options.scene);
    scene = scene.substring(scene.lastIndexOf("/")+1);
    console.log(scene)
    this.setData({scene})
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    const scene = this.data.scene;
    const app = getApp();

    if(!scene) return;
    wx.showModal({
      title: "授权登陆",
      content: "确认授权网页端登陆吗？",
      success(res) {
        if (res.confirm){
          const url = app.globalData.url + "/auth/authencate/" + scene + "/";
          console.log("url: " + url)

          wx.request({
            url: url,
            header: {
              "Session": wx.getStorageSync("Session")
            },
            success(res){
              const payload = res.data;
              console.log(payload)
              let dialog = null;
              if(payload.code != 0){
                dialog = wx.showToast({
                  title: payload.errmsg,
                  icon: "error",
                  duration: 3000
                })
              }else{
                dialog = wx.showToast({
                  title: '登陆成功',
                  icon: "success",
                  duration: 3000
                })
              }
              setTimeout(() => {
                wx.switchTab({
                  url: '/pages/setting/setting',
                })
              }, 3000)
            },
            fail(res){
              wx.showToast({
                title: res.errMsg,
                icon: "error",
                duration: 3000
              })
              setTimeout(() => {
                wx.switchTab({
                  url: '/pages/setting/setting',
                })
              }, 3000)
            }
          })
        }
      }
    })
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {},

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {},

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {},

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {},

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {},

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {}
})