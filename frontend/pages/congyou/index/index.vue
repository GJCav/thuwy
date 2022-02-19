<template>
	<view>
		<!-- 浮动按钮 -->
		<uni-fab v-if="admin" :popMenu="false" :pattern="{buttonColor:'#5800A6'}" @fabClick="addNew()"></uni-fab>
		<!-- 具体从游坊信息 -->
		
	</view>
</template>

<script>
	const app=getApp()
	export default {
		data() {
			return {
				admin:false,
				page:1
			}
		},
		onLoad(e){
			uni.request({
				header: {
					'content-type': 'application/json; charset=utf-8',
					'cookie': wx.getStorageSync('cookie')
				},
				url:app.globalData.url.backend+'/lecture/?p=1',
				method:'GET',
			}).then(res=>{
				console.log(res)
			})
			this.admin=e.admin
		},
		methods: {
			addNew(){
				uni.navigateTo({
					url:'../info/info?id=0'
				})
			}
		}
	}
</script>

<style>

</style>
