// pages/info/info.js
Page({
    data: {
        md_info: '',
        title: '',
    },
    onLoad: function (options) {
        let pages = getCurrentPages();
        let prevPage = pages[pages.length - 2];
        this.setData({
            md_info:prevPage.data.md_intro,
            title: options.title
        })
        wx.setNavigationBarTitle({
            title: this.data.title
        })
    },
})