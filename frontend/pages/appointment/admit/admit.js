// pages/appointment/admit/admit.js
const app = getApp()

Page({
  data: {
    disable: [], //无法预约的时间段
    name: '',
    id: 0,
    md_intro: '',
    rsv_method: 3,
    choose_method: 0,

    date_index: 0,
    st_index: "00:00",
    ed_index: "00:00",

    reason: '',
    list: [],
    calendar: [], //固定预约日期表
    flex_calendar: [], //自由预约日期表
    items1: [{
        value: '1',
        name: '上午（8：00-12：00）  '
      },
      {
        value: '2',
        name: '下午（13：00-17：00）  '
      },
      {
        value: '3',
        name: '晚上（18：00-23：00）  '
      }
    ],
    items2: [{
      value: '4',
      name: '周末全天    '
    }]
  },
  onLoad: function (options) {
    wx.showLoading({
      mask: true,
      title: '加载中',
    })
    wx.enableAlertBeforeUnload({
      message: '您确定要离开此页面吗？已经填写的信息将会丢失',
    })
    this.setData({
      id: parseInt(options.id),
      disable: [
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true]
      ],
    })
    wx.setNavigationBarTitle({
      title: '提交申请'
    })
    //计算接下来七天的日期
    let that = this;

    function getThisMonthDays(year, month) {
      return new Date(year, month, 0).getDate();
    }
    // 计算每月第一天是星期几
    function getFirstDayOfWeek(year, month) {
      return new Date(Date.UTC(year, month - 1, 1)).getDay();
    }
    const date = new Date();
    const cur_year = date.getFullYear();
    const cur_month = date.getMonth() + 1;
    const cur_date = date.getDate();
    const weeks_ch = ['日', '一', '二', '三', '四', '五', '六'];
    //利用构造函数创建对象
    function calendar(date, week) {
      var y = cur_year;
      var m = cur_month;
      var d = date;
      if (d > monthLength) {
        if (m == 12) {
          y = y + 1;
          m = 1;
          d = d - 31;
        } else {
          y = y;
          m = m + 1;
          d = d - monthLength;
        }
      }
      this.date = String(y) + ((m < 10) ? '-0' : '-') + String(m) + ((d < 10) ? '-0' : '-') + String(d);
      this.week = '星期' + week;
    }
    //当前月份的天数
    var monthLength = getThisMonthDays(cur_year, cur_month)
    //当前月份的第一天是星期几
    var week = getFirstDayOfWeek(cur_year, cur_month)
    var x = week;
    for (var i = 1; i <= monthLength + 8; i++) {
      if (x > 6) {
        x = 0;
      }
      //利用构造函数创建对象
      that.data.calendar[i] = new calendar(i, [weeks_ch[x]][0])
      x++;
    }
    var t = that.data.calendar[cur_date].week
    var flag = that.data.calendar.slice(cur_date, cur_date + 7)
    for (var i = 0; i < 7; ++i) {
      let item = flag[i]
      item.whole = item.date + '（' + item.week + '）'
    }
    that.setData({
      flex_calendar: flag,
      calendar: flag.slice((t == '星期六' ? 2 : (t == '星期日') ? 1 : 0), (t == '星期六' ? 2 : (t == '星期日') ? 1 : 0) + (t == '星期六' ? 5 : (t == '星期日') ? 6 : 7))
    })
    that.getitem().then(function () {
      that.getrsvs().then(function () {
        wx.hideLoading()
      }).catch(function (res) {
        console.log(res.data.code, res.data.errmsg)
        wx.showToast({
          title: '信息读取失败',
          icon: 'error',
          duration: 1500
        })
        setTimeout(function () {
          wx.navigateBack({
            delta: 1
          })
        }, 1500)
      })
    }).catch(function (res) {
      console.log(res.data.code, res.data.errmsg)
      wx.showToast({
        title: '信息读取失败',
        icon: 'error',
        duration: 1500
      })
      setTimeout(function () {
        wx.navigateBack({
          delta: 1
        })
      }, 1500)
    })
  },
  //封装接口
  getitem() { //读取物品信息
    let that = this
    return new Promise(function (resolve, reject) {
      wx.request({
        url: app.globalData.url + '/item/' + that.data.id,
        method: 'GET',
        success: (res) => {
          console.log(res)
          let those = res.data
          if (those.code == 0) {
            that.setData({
              name: those.item.name,
              md_intro: those.item['md-intro'],
              rsv_method: those.item['rsv-method'],
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
    })
  },
  //读取并处理预约信息
  getrsvs() {
    let that = this
    return new Promise(function (resolve, reject) {
      wx.request({
        url: app.globalData.url + '/item/' + that.data.id + '/reservation',
        method: 'GET',
        success: (res) => {
          if (res.data.code == 0) {
            var tmp = that.data.disable;
            for (var i = 0; i < that.data.calendar.length; ++i) { //枚举接下来七天的日期
              var the_date = that.data.calendar[i];
              for (var j = 0; j < res.data.rsvs.length; ++j) { //枚举未来七天内的预约
                if (parseInt(res.data.rsvs[j].state / 4) % 2 == 0) { //判断预约是否已经结束
                  var rsv_time = res.data.rsvs[j].interval;
                  for (var k = 0; k < rsv_time.length; ++k) { //枚举具体的预约时间段
                    if (rsv_time[k].slice(0, -2) == the_date.date) {
                      tmp[i][rsv_time[k].slice(-1) - 1] = false
                      if (the_date.week == '星期六')
                        tmp[i + 1][rsv_time[k].slice(-1) - 1] = false;
                    }
                  }
                }
              }
            }
            that.setData({
              disable: tmp
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
    })
  },
  //输入预约信息
  inputmethod(e) {
    this.setData({
      choose_method: e.detail.value
    });
  },
  inputwhy: function (e) {
    this.setData({
      reason: e.detail.value
    });
  },
  date_change(e) {
    console.log('选择日期为', e.detail.value)
    this.setData({
      date_index: e.detail.value
    })
  },
  st_change(e) {
    console.log('选择开始时间为', e.detail.value)
    this.setData({
      st_index: e.detail.value
    })
  },
  ed_change(e) {
    console.log('选择结束时间为', e.detail.value)
    this.setData({
      ed_index: e.detail.value
    })
  },
  appoint: function () {
    console.log(this.selectedIdxs)
    this.setData({
      list: []
    });
    if (this.data.choose_method == 0) {
      wx.showToast({
        title: '未选择预约方式',
        icon: 'error'
      })
    } else if (this.data.choose_method == 1 && this.selectedIdxs == null) {
      wx.showToast({
        title: '未选择预约时间',
        icon: 'error'
      })
    } else if (this.data.choose_method == 2 && this.data.st_index >= this.data.ed_index) {
      wx.showToast({
        title: '预约时间不合理',
        icon: 'error',
      })
    } else if (this.data.reason == '') {
      wx.showToast({
        title: '未填写预约理由',
        icon: 'error'
      })
    } else {
      wx.showLoading({
        mask: true,
        title: '提交中',
      })
      if (this.data.choose_method == 1) { //固定时间段预约
        for (var i = 0; i < this.selectedIdxs.length; i++) {
          var d = parseInt(this.selectedIdxs[i] / 10)
          var m = this.selectedIdxs[i] % 10
          if (this.data.calendar[d].week == '星期日')
            d = this.data.calendar[d - 1].date
          else
            d = this.data.calendar[d].date
          var addone = [d + ' ' + m]
          this.setData({
            list: this.data.list.concat(addone)
          });
        }
      } else { //自由时间段预约
        this.setData({
          list: this.data.flex_calendar[this.data.date_index].date + ' ' + this.data.st_index + '-' + this.data.ed_index,
        })
      }
    }
    console.log(this.data.list)
    wx.request({
      header: {
        'content-type': 'application/json; charset=utf-8',
        'cookie': wx.getStorageSync('cookie')
      },
      url: app.globalData.url + '/reservation',
      method: 'POST',
      data: {
        'item-id': this.data.id,
        reason: this.data.reason,
        method: this.date.choose_method,
        interval: this.data.list
      },
      success: function (res) {
        console.log(res)
        if (res.data.code == 0) {
          wx.hideLoading()
          wx.showToast({
            title: '提交成功',
            icon: 'success',
            duration: 1500,
            mask: true
          })
          setTimeout(function () {
            wx.navigateBack({
              delta: 1
            })
          }, 1500)
        } else {
          console.log(res.data.code, res.data.errmsg)
          wx.hideLoading();
          wx.showToast({
            title: '提交失败',
            icon: 'error'
          })
        }
      },
      fail: function (res) {
        console.log(res.data.code, res.data.errmsg)
        wx.hideLoading();
        wx.showToast({
          title: '网络异常',
          icon: 'error'
        });
      }
    })
  },
  checkboxChange(e) {
    console.log('选中时间为：', e.detail.value)
    this.selectedIdxs = e.detail.value
  },
})