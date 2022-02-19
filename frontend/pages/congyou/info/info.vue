<template>
	<view>
		<weiyang-forms>
			
		</weiyang-forms>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				
			}
		},
		methods: {
			
		},
		onLoad(e) {
			if(e.id==0){
				uni.setNavigationBarTitle({
					title:'新建活动信息'
				})
			}
		}
	}
</script>

<style>

</style>
