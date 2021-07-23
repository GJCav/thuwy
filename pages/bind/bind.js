// bind.js
// 获取应用实例
const app = getApp()

Page({
  data:{
    titleInfo:'请如实填写以下信息',
    name:'',
    id:'',
    clz:''
  },
  onLoad(){
    wx.setNavigationBarTitle({
      title: '绑定信息'
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
  addUser(e){
    console.log(app.globalData.url),
    wx.request({
      url: app.globalData.url+'/bind',
      method: "POST",
      data:{
        id:this.data.id,
        name:this.data.name,
        clazz:this.data.clz
      },
      success(res){
        console.log('绑定成功');
        if(res.data.code==0){
          wx.showToast({
            title: '绑定成功',
            icon: 'success',
            duration: 1500
          });
          setTimeout(function () {
              wx.navigateBack({
              delta: 1
            })
          }, 1500) 
        }
        else{

        }
      }
    })  
  }
})