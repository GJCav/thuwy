// pages/equip/equip.js
const app = getApp()
const util = require('../../utils/util.js') 
Page({
  data: {
    item_id: 0,
    name: '',
    available: true,
    brief_intro: '',
    md_intro:'',
    rsv_method: 0,
    attr: 0,
    group:'无分组',

    //显示特殊属性
    show: false,
    item_feature: [],
    item_group:[],

    havepic: false,
    thumbnail: '',
    uploadurl: '',
    finalurl: '',

    methods: [{
      value: 1,
      checked: false,
      can: true,
      name: '固定时间段预约'
    }, {
      value: 2,
      checked: false,
      can: true,
      name: '自由时间段预约'
    }]
  },
  //输入保存各种信息
  inputname: function (e) {
    this.setData({
      name: e.detail.value
    });
  },
  inputintro: function (e) {
    this.setData({
      brief_intro: e.detail.value
    });
  },
  inputmd: function (e) {
    this.setData({
      md_intro: e.detail.value
    });
  },
  inputcan: function (e) {
    this.data.available = e.detail.value
  },
  inputgroup:function(e){
    this.setData({
      group:this.data.item_group[e.detail.value]
    })
  },
  rsvmethod: function (e) {
    let sel = e.detail.value
    var sum = 0
    for (var i = 0; i < sel.length; ++i)
      sum = sum + parseInt(sel[i])
    this.setData({
      rsv_method: sum
    })
    console.log(this.data.rsv_method)
  },
  //展示特殊属性
  show_feature() {
    this.setData({
      show: true
    })
  },
  //展示放大后图片
  preview(e){
    wx.previewImage({
      urls: [e.currentTarget.dataset['url']],
    })
  },
  //添加特殊属性
  add_feature(e) {
    this.setData({
      attr: this.data.attr + (1 << e.currentTarget.dataset['id']),
      show: false
    })
  },
  del_feature(e) {
    this.setData({
      attr: this.data.attr - (1 << e.currentTarget.dataset.id),
    })
  },
  //预览详细介绍（md格式）
  showmd() {
    wx.navigateTo({
      url: '../info/info?title=详情预览&type=0',
    })
  },
  choosepic: function (e) {
    wx.chooseImage({
      count: 1,
      sourceType: [e.currentTarget.dataset.way],
      success: (res) => {
        this.setData({
          thumbnail: res.tempFilePaths[0],
          havepic: true
        });
        console.log(this.data.thumbnail)
      },
      fail: (res) => {
        console.log(res)
        this.setData({
          havepic: false
        });
        wx.showToast({
          title: '读取失败',
          icon: 'error',
          duration:1000,
          mask: true
        })
      },
    })
  },
  onLoad: function (options) {
    this.setData({
      item_id: options.id,
      item_feature: app.globalData.item_feature,
      item_group:app.globalData.item_group.slice(1,-1).concat(['无分组'])
    })
    if (options.id != 0) {
      wx.setNavigationBarTitle({
        title: '修改设备'
      })
      wx.showLoading({
        mask: true,
        title: '加载中',
      })
      wx.request({
        url: app.globalData.url + '/item/' + this.data.item_id + '/',
        method: 'GET',
        success: (res) => {
          let those = res.data
          if (those.code == 0) {
            this.setData({
              name: those.item.name,
              brief_intro: those.item['brief-intro'],
              md_intro: those.item['md-intro'],
              rsv_method: those.item['rsv-method'],
              thumbnail: those.item.thumbnail,
              available: those.item.available,
              attr: those.item.attr,
              group:those.item.group
            })
            let that = this.data
            if (that.rsv_method % 2 == 1) {
              this.setData({
                'methods[0].checked': true
              })
            }
            if ((that.rsv_method >> 1) % 2 == 1) {
              this.setData({
                'methods[1].checked': true
              })
            }
            wx.hideLoading()
          } else {
            wx.hideLoading()
            util.show_error(res)
            setTimeout(function () {
              wx.navigateBack({
                delta: 1
              })
            }, 1500)
          }
        },
        fail: (res) => {
          wx.hideLoading()
          util.show_error(res)
          setTimeout(function () {
            wx.navigateBack({
              delta: 1
            })
          }, 1500)
        }
      })
    } else {
      wx.setNavigationBarTitle({
        title: '添加设备'
      })
    }
  },
  //封装获取上传地址
  getuploadurl() {
    let that = this
    return new Promise(function (resolve, reject) {
      if (that.data.havepic) {
        console.log(app.globalData.picurl + '/uploadurl/' + that.data.name + '.jpg')
        wx.request({
          url: app.globalData.picurl + '/uploadurl/' + that.data.name + '.jpg',
          method: 'GET',
          header: {
            'content-type': 'text/plain',
          },
          success: (res) => {
            console.log(res)
            if (res.statusCode == 200 & res.data.code == 0) {
              that.setData({
                uploadurl: res.data.data,
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
      } else{
        resolve()
      }
    })
  },
  //封装上传文件
  upfile() {
    let that = this
    return new Promise(function (resolve, reject) {
      if (that.data.havepic) {
        wx.uploadFile({
          url: app.globalData.picurl + '/upload/' + that.data.name + '.jpg',
          filePath: that.data.thumbnail,
          name: 'file', // 这里固定为"file"
          success: (res) => {
            var obj = JSON.parse(res.data)
            if (obj.code == 0) {
              that.setData({
                finalurl: obj.data
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
      } else {
        resolve()
      }
    })
  },
  //提交信息
  addit() {
    let that = this
    if (that.data.mame == '' || that.data.rsv_method == 0 || that.data.brief_intro == '' || that.data.thumbnail == ''||that.data.group==' ') {
      wx.showToast({
        title: '信息未填写完整',
        icon: 'error',
        duration: 1500,
        mask:true
      })
    } else if (that.data.item_id == 0) { //添加物品
      wx.showLoading({
        title: '提交中',
        mask: true
      })
      that.getuploadurl().then(function () {
        that.upfile().then(function () {
          console.log(that.data.finalurl)
          wx.request({
            header: {
              'content-type': 'application/json; charset=utf-8',
              'Session': wx.getStorageSync('Session')
            },
            url: app.globalData.url + '/item/',
            method: "POST",
            data: {
              name: that.data.name,
              'brief-intro': that.data.brief_intro,
              'md-intro': that.data.md_intro,
              thumbnail: that.data.finalurl,
              'rsv-method': that.data.rsv_method,
              attr: that.data.attr,
              group:that.data.group
            },
            success: (res) => {
              if (res.data.code == 0) {
                wx.hideLoading();
                wx.showToast({
                  mask: true,
                  title: '添加成功',
                  icon: 'success',
                  duration: 1500
                });
                setTimeout(function () {
                  wx.navigateBack({
                    delta: 1
                  })
                  let pages = getCurrentPages();
                  let prevPage = pages[pages.length - 2];
                  prevPage.refresh()
                }, 1500)
              } else {
                wx.hideLoading()
                util.show_error(res)
              }
            },
            fail: (res) => {
              wx.hideLoading();
              util.show_error(res)
            }
          })
        }).catch(function (res) {
          console.log(res)
          wx.hideLoading()
          wx.showToast({
            title: '图片上传失败',
            icon: 'error',
            duration: 1500,
            mask:true
          })
        })
      }).catch(function (res) {
        console.log(res)
        wx.hideLoading()
        wx.showToast({
          title: '图片服务器错误',
          icon: 'error',
          duration: 1500,
          mask:true
        })
      })
    } else { //修改物品
      wx.showLoading({
        title: '提交中',
        mask: true
      })
      that.getuploadurl().then(function () {
        that.upfile().then(function () {
          console.log(that.data.finalurl)
          var final_data = {
            name: that.data.name,
            'brief-intro': that.data.brief_intro,
            'md-intro': that.data.md_intro,
            'rsv-method': that.data.rsv_method,
            available: that.data.available,
            attr: that.data.attr,
            group:that.data.group
          }
          if (that.data.havepic) final_data.thumbnail = that.data.finalurl
          wx.request({
            header: {
              'content-type': 'application/json; charset=utf-8',
              'Session': wx.getStorageSync('Session')
            },
            url: app.globalData.url + '/item/' + that.data.item_id + '/',
            method: "POST",
            data: final_data,
            success: (res) => {
              if (res.data.code == 0) {
                wx.hideLoading();
                wx.showToast({
                  mask: true,
                  title: '修改成功',
                  icon: 'success',
                  duration: 1500
                });
                setTimeout(function () {
                  wx.navigateBack({
                    delta: 1
                  })
                  let pages = getCurrentPages();
                  let prevPage = pages[pages.length - 2];
                  prevPage.refresh()
                }, 1500)
              } else {
                wx.hideLoading()
                util.show_error(res)
              }
            },
            fail: (res) => {
              wx.hideLoading();
              util.show_error(res)
            }
          })
        }).catch(function (res) {
          console.log(res)
          wx.hideLoading()
          wx.showToast({
            title: '图片上传失败',
            icon: 'error',
            duration: 1500,
            mask:true
          })
        })
      }).catch(function (res) {
        console.log(res)
        wx.hideLoading()
        wx.showToast({
          title: '图片服务器错误',
          icon: 'error',
          duration: 1500,
          mask:true
        })
      })
    }
  }
})