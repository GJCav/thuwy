<template>
	<view>
		
	</view>
</template>

<script>
	const app=getApp()
	export default {
		data() {
			return {
				
			}
		},
		methods: {
			
		},
		onLoad(e){
			uni.setNavigationBarTitle({
				title:''
			})
			uni.request({
				url:app.globalData.url.backend+'',
				method:'GET',
				data:{
					
				}
			}).then(res=>{
				console.log(res)
				this.data=res.data
			}).catch(err=>{
				console.log(err)
			})
		}
	}
</script>

<style>

</style>
