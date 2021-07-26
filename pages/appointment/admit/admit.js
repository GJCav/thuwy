// pages/appointment/admit.js
Page({
  data: {
    equip: '相机',
    method1:'checkboxChange',
    method2:'specialChange',
    specialchecked: false,
    reason: '',
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
      //当循环完一周后，初始化再次循环
      if (x > 6) {
        x = 0;
      }
      //利用构造函数创建对象
      that.data.calendar[i] = new calendar(i, [weeks_ch[x]][0])
      x++;
    }
    //限制要渲染的日历数据天数为7天以内（用户体验）
    var flag = that.data.calendar.splice(cur_date + 1, 7)
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
    console.log('选中的索引列表')
    console.log(this.selectedIdxs || [])
  },
  checkboxChange(e) {
    console.log('checkbox发生change事件，携带value值为：', e.detail.value)
  },
  specialChange(e) {
    console.log('checkbox发生change事件，携带value值为：', e.detail.value)
    if (e.detail.value!='')
      this.setData({
        specialchecked: true
      })
    else
      this.setData({
        specialchecked: false
      })
  }
})