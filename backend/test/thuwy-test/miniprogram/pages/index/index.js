// pages/index/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    urlbase: "http://127.0.0.1:5000/",
    reqScopeStr: "",
    authCode: ""
  },
  onLogin(){
    let data = this.data
    wx.login({
      timeout: 5000,
      success(res){
        if (res.code){
          wx.request({
            url: data.urlbase + "login/",
            timeout: 2000,
            data: {code: res.code},
            method: 'POST',
            success(o){
              wx.setStorageSync('cookie', o.cookies[0])
              console.log(`Cookie: ${o.cookies[0]}`)
            },
            fail(){
              console.log('fail to connent backend')
            }
          })
        }else{
          console.log('wx.login fail ' + res.errMsg)
        }
      }
    })
  },
  onBind(){
    let urlbase = this.data.urlbase;
    wx.request({
      url: urlbase + 'bind/',
      method:'POST',
      header: {
        'content-type': 'application/json; charset=utf-8',
        'cookie': wx.getStorageSync('cookie') // 这里取出储存的登陆信息，传给服务器
      },
      data: {
        id: 2020013059,
        name: '顾家铭',
        clazz: '未央-微软工01'
      },
      success(res){
        console.log(res.data)
      }
    })
  },
  onGetProfile(){
    let urlbase = this.data.urlbase;
    wx.request({
      url: urlbase + 'profile/',
      header: {
        'content-type': 'application/json; charset=utf-8',
        'cookie': wx.getStorageSync('cookie') // 这里取出储存的登陆信息，传给服务器
      },
      success(res){
        console.log(res.data)
      }
    })
  },

  reqScopeStr(e){
    this.setData({reqScopeStr: e.detail.value})
  },
  authCode(e){
    this.setData({authCode: e.detail.value})
  },
  onReqOAuth(){
    let urlbase = this.data.urlbase;
    let scopes = this.data.reqScopeStr.split(" ");
    let that = this;
    console.log(`request scopes: ${scopes}`)
    wx.request({
      url: urlbase + 'oauth/authorize/',
      method: 'POST',
      data: {
        scopes: scopes
      },
      success(res){
        console.log(res.data);
        let json = res.data
        if(json.code != 0) return;
        that.setData({authCode: json.auth_code});
      },
      fail(res){
        console.log('fail')
        console.log(res)
      }
    })
  },
  onPollOAuth(){
    let baseurl = this.data.urlbase;
    let authCode = this.data.authCode;
    let url = baseurl+'oauth/authorize/'+authCode+'/'
    console.log('Poll on '+authCode)
    wx.request({
      url: url,
      success(res){
        console.log(res.data);
      },
      fail(res){
        console.log(res);
        console.log("fail")
      }
    })
  },
  onGrantOAuth(){
    let baseurl = this.data.urlbase;
    let authCode = this.data.authCode;
    let url = baseurl+'oauth/authorize/'+authCode+'/'
    wx.request({
      url: url,
      method: "POST",
      header: {
        'cookie': wx.getStorageSync('cookie') // 这里取出储存的登陆信息，传给服务器
      },
      data: {authorize: "grant"},
      success(res){
        console.log(res.data)
        let json = res.data
        if(json.code != 0) return;
        console.log(`token: ${json.token}`)
        console.log(`expire at: ${new Date(json.expire_at).toLocaleString()}`)
      },
      fail(res){
        console.log(res)
        console.log('fail')
      }
    })
  },
  onRejectOAuth(){
    let baseurl = this.data.urlbase;
    let authCode = this.data.authCode;
    let url = baseurl+'oauth/authorize/'+authCode+'/';
    wx.request({
      url: url,
      method: "POST",
      header: {
        'cookie': wx.getStorageSync('cookie') // 这里取出储存的登陆信息，传给服务器
      },
      data: {authorize: "reject"},
      success(res){
        console.log(res.data)
        let json = res.data
      },
      fail(res){
        console.log(res)
        console.log('fail')
      }
    })
  }
})