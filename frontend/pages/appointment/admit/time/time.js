// pages/appointment/admit/time/time.js
Page({
    data: {
        st: 0,
        ed: 0,
        have_st: false,
        have_ed: false,
        st_index: "00:00",
        ed_index: "00:00",
    },
    onLoad: function (options) {
        wx.setNavigationBarTitle({
            title: '选择时间'
        })
        wx.enableAlertBeforeUnload({
            message: '您确定要离开此页面吗？已经填写的信息将会丢失',
        })
        this.setData({
            st: options.st,
            ed: options.ed
        })
        console.log(this.data.st, this.data.ed)
    },
    st_change(e) {
        console.log('选择开始时间为', e.detail.value)
        this.setData({
            st_index: e.detail.value,
            have_st: true
        })
    },
    ed_change(e) {
        console.log('选择结束时间为', e.detail.value)
        this.setData({
            ed_index: e.detail.value,
            have_ed: true
        })
    },
    //提交时间
    sure() {
        wx.showLoading({
            title: '处理中',
            mask: true
        })
        if(this.data.st_index==this.data.ed_index)
        {
            wx.hideLoading()
            wx.showToast({
            mask: true,
            title: '时间段过短',
            icon: 'error',
            duration: 1000
          })
          return;
        }
        let pages = getCurrentPages();
        let prevPage = pages[pages.length - 2];
        let ctx = prevPage.data.ctx
        let width = prevPage.data.whole_width
        let height = prevPage.data.each_height

        function change_time(t) {
            return height / 60 * ((parseInt(t.slice(0, 2))-8) * 60 + parseInt(t.slice(3))) + 40
        }
        if (prevPage.data.final_st != '') {
            ctx.clearRect(parseInt(width / 2), change_time(prevPage.data.final_st), parseInt(width / 2), change_time(prevPage.data.final_ed) - change_time(prevPage.data.final_st))
            prevPage.drawRect(2, prevPage.data.final_st, prevPage.data.final_ed, false)
        }
        prevPage.setData({
            final_st: this.data.st_index,
            final_ed: this.data.ed_index
        })
        //重绘选择区域图
        prevPage.drawRect(3, prevPage.data.final_st, prevPage.data.final_ed, true)
        wx.hideLoading()
        wx.showToast({
            mask: true,
            title: '选择成功',
            icon: 'success',
            duration: 1000
          })
          console.log(prevPage.data.final_st,prevPage.data.final_ed)
        wx.navigateBack({
            delta: 1
        })
    }
})