// pages/appointment/admit.js
Page({
  data: {
    name: '',
    id:'',
    reason: '',
    list: [],
    calendar: [],
    width: 0,
    currentIndex: 0,
    currentTime: 0,
    items1: [{
        value: '1',
        name: '上午（8：00-12：00）'
      },
      {
        value: '2',
        name: '下午（13：00-17：00）'
      },
      {
        value: '3',
        name: '晚上（18：00-23：00）'
      }
    ],
    items2: [{
      value: '4',
      name: '周末两日全天'
    }]
  },
  onLoad: function (options) {
    this.setData({
      id:options.id,
      name:options.name
    })
    wx.setNavigationBarTitle({
      title: '提交申请'
    })
    var that = this;

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
      if (date > monthLength) {
        if (cur_month == 12)
          this.date = (cur_year + 1) + '-1-' + (date - 31);
        else
          this.date = cur_year + '-' + (cur_month + 1) + '-' + (date - monthLength);
      } else {
        this.date = cur_year + '-' + cur_month + '-' + date;
      }
      this.week = '星期' + week;
    }
    //当前月份的天数
    var monthLength = getThisMonthDays(cur_year, cur_month)
    //当前月份的第一天是星期几
    var week = getFirstDayOfWeek(cur_year, cur_month)
    var x = week;
    for (var i = 1; i <= monthLength + 7; i++) {
      if (x > 6) {
        x = 0;
      }
      //利用构造函数创建对象
      that.data.calendar[i] = new calendar(i, [weeks_ch[x]][0])
      x++;
    }
    //限制要渲染的日历数据天数为7天以内
    var flag = that.data.calendar.splice(cur_date + 1, that.data.calendar[cur_date].week == '星期六' ? 8 : 7)
    that.setData({
      calendar: flag
    })
  },
  inputwhy: function (e) {
    this.setData({
      reason: e.detail.value
    });
  },
  appoint: function () {
    console.log(this.selectedIdxs)
    this.setData({
      list: []
    });
    if (this.selectedIdxs == null) {
      wx.showToast({
        title: '未选择预约时间',
        icon: 'error'
      })
    } else {
      for (var i = 0; i < this.selectedIdxs.length; i++) {
        var d = Math.floor(this.selectedIdxs[i] / 10)
        var m = this.selectedIdxs[i] % 10
        if (this.data.calendar[d].week == '星期日')
          d = this.data.calendar[d - 1].date
        else
          d = this.data.calendar[d].date
        var addone = [d + ' ' + m]
        this.setData({
          'list': this.data.list.concat(addone)
        });
      }
      console.log(this.data.list)
      wx.request({
        url: app.globalData.url+'/reserve',
        method:'POST',
        data:{
          'item-id':this.data.id,
          reason:this.data.reason,
          method:1,
          interval:this.data.list
        },
        success: function (res) {
          if(res.code==0)
          {
            wx.showToast({
              title: '提交成功',
              icon:'success'
            })
          }
          else{
            console.log(res.code,res.errmsg)
          }
        }
      })
    }
  },
  checkboxChange(e) {
    console.log('checkbox发生change事件，携带value值为：', e.detail.value)
    this.selectedIdxs = e.detail.value
  },
})