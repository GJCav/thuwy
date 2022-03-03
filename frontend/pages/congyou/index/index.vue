<template>
	<view>
		<!-- 浮动按钮 -->
		<uni-fab v-if="admin" :popMenu="false" :pattern="{buttonColor:'#5800A6'}" @fabClick="addNew()"></uni-fab>
		<!-- 具体从游坊信息 -->
		<view class="col-container" style="margin-bottom:10px;">
			<weiyang-card v-for="item in whole_data" :key="item.id" :text="item.detail" :pattern="item.pattern" url="">
			</weiyang-card>
		</view>
		
	</view>
</template>

<script>
	const app = getApp()
	import utils from '../../../common/utils.js'
	export default {
		data() {
			return {
				admin: false,
				page: 1,
				key: '',
				load_more: 'more',
				whole_data: []
			}
		},
		onLoad(e) {
			this.admin = e.admin
		},
		onShow() {
			this.refreshDate(1, this.key)
		},
		onPullDownRefresh() {
			this.refreshDate(1, this.key)
		},
		onReachBottom() {
			if (this.load_more != 'noMore') {
				this.load_more = 'loading'
				this.refreshDate(++this.page, this.key)
			}
		},
		methods: {
			// 获取数据
			refreshDate(page, key) {
				uni.showLoading({
					title: '加载中',
					mask: true
				})
				if (page == 1) {
					this.page = 1
					this.whole_data = []
				}
				uni.request({
					header: {
						'content-type': 'application/json; charset=utf-8',
						'cookie': wx.getStorageSync('cookie')
					},
					url:app.globalData.url.backend+'/lecture/?p=1',
					method:'GET',
					data: {
						page_num: page,
						keywords: key || ''
					}
				}).then(res => {
					console.log(res)
					if (res.data.code == 0) {
						let raw_data = res.data.lectures
						let whole = []
						for (let i = 0, len = raw_data.length; i < len; i++) {
							let item = raw_data[i]
							whole.push({
								id: item.lecture_id,
								pattern: 31,
								detail: {
									title: '从游坊第' + item.lecture_id + '讲',
									theme: item.teacher + '：' + item.theme,
									content: utils.changeTime(item.holding_time) + item.position,
									info: utils.changeTime(item.deadline) + '截止',
									tag: '可报名'
								}
							})
						}
						if (whole.length > 0) {
							this.whole_data = this.whole_data.concat(whole)
							this.load_more = 'more'
						} else {
							this.load_more = 'noMore'
						}
						uni.hideLoading()
					} else {
						throw res
					}
				}).catch(err => {
					utils.errInfo(err, '网络加载失败')
				})
			},
			// 转到创建页面
			addNew() {
				uni.navigateTo({
					url: '../info/info?admin=' + this.admin
				})
			}
		}
	}
</script>

<style>

</style>
